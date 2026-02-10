"""
Albion Online Profit Analyzer
Fetches historical market data from Albion Online Data Project API
and calculates profit margins for crafted items
"""

import asyncio
import aiohttp
import pandas as pd
from datetime import datetime
import random
import sys
import io

# Import configuration and utilities
from config import (
    BASE_URL, BLACK_MARKET, return_rate,
    retries, chunk_size, timeout, concurrent_requests,
    normal_wait_min, normal_wait_max, throttle_wait_base, throttle_wait_max
)
from calculator import get_recipe_for_item, calculate_cost, generate_all_items
from item_lists import ALL_ITEM_NAMES, DEFAULT_TIERS, DEFAULT_ENCHANTS

# Windows compatibility
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # Fix encoding issues on Windows
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


async def fetch_item_history_data(session, item_id, sem):
    """
    Fetch historical market data for a single item with 429 throttling protection.

    Args:
        session (aiohttp.ClientSession): HTTP session for making requests
        item_id (str): Item ID to fetch data for
        sem (asyncio.Semaphore): Semaphore to limit concurrent requests

    Returns:
        dict: JSON response containing historical price data
        None: If fetch fails after all retries
    """
    url = f"{BASE_URL}/api/v2/stats/history/{item_id}"
    params = {
        "locations": BLACK_MARKET,
        "time-scale": 6
    }

    attempt = 0
    async with sem:
        while attempt <= retries:
            try:
                async with session.get(url, params=params, timeout=timeout) as resp:
                    if resp.status == 200:
                        print(f"✅ 履歴取得成功: {item_id}", flush=True)
                        # Normal wait after success
                        await asyncio.sleep(random.uniform(normal_wait_min, normal_wait_max))
                        return await resp.json()
                    elif resp.status == 429:
                        attempt += 1
                        wait_time = min(throttle_wait_base * attempt + random.uniform(0, 2), throttle_wait_max)
                        print(f"⚠️ 429制限: {item_id} 再試行({attempt}/{retries}) 待機 {wait_time:.1f}s", flush=True)
                        await asyncio.sleep(wait_time)
                    else:
                        attempt += 1
                        wait_time = random.uniform(normal_wait_min, normal_wait_max)
                        print(f"⚠️ HTTP {resp.status}: {item_id} 再試行({attempt}/{retries}) 待機 {wait_time:.1f}s", flush=True)
                        await asyncio.sleep(wait_time)
            except Exception as e:
                attempt += 1
                wait_time = random.uniform(normal_wait_min, normal_wait_max)
                print(f"⚠️ 例外: {item_id} → {e} 再試行({attempt}/{retries}) 待機 {wait_time:.1f}s", flush=True)
                await asyncio.sleep(wait_time)
    print(f"❌ 履歴取得失敗: {item_id}", flush=True)
    return None


async def get_latest_timeseries_data(items, time_scale=6, process_chunk_callback=None):
    """
    Fetch time series data for multiple items with chunking and throttling protection.

    Args:
        items (list): List of item IDs to fetch
        time_scale (int): Time scale parameter for API (6 = daily)
        process_chunk_callback: Optional callback function to process each chunk's results

    Returns:
        list: List of dictionaries containing item data with latest prices and trade counts
    """
    results = []

    sem = asyncio.Semaphore(concurrent_requests)
    failed_items = []

    async with aiohttp.ClientSession() as session:
        # Process in chunks to avoid overwhelming the API
        for i in range(0, len(items), chunk_size):
            chunk = items[i:i + chunk_size]
            print(f"\n📦 チャンク {i//chunk_size + 1}/{(len(items) + chunk_size - 1)//chunk_size} 処理中...", flush=True)

            # Fetch historical data (with trade counts)
            tasks = [fetch_item_history_data(session, item, sem) for item in chunk]
            chunk_results = await asyncio.gather(*tasks)

            # Process data
            chunk_data = []
            for item, data in zip(chunk, chunk_results):
                if data:
                    # Process data by quality level
                    for quality_record in data:
                        quality = quality_record.get('quality', 'unknown')
                        time_series = quality_record.get('data', [])

                        if time_series:
                            # Get latest entry (sorted by timestamp descending)
                            sorted_data = sorted(time_series,
                                               key=lambda x: x.get('timestamp', ''),
                                               reverse=True)
                            latest_data = sorted_data[0] if sorted_data else None

                            if latest_data:
                                item_result = {
                                    'item_id': item,
                                    'quality': quality,
                                    'latest_timestamp': latest_data.get('timestamp'),
                                    'avg_price': latest_data.get('avg_price', 0),
                                    'item_count': latest_data.get('item_count', 0),
                                    'location': BLACK_MARKET
                                }
                                results.append(item_result)
                                chunk_data.append(item_result)
                else:
                    failed_items.append(item)

            # Call callback with chunk data if provided
            if process_chunk_callback and chunk_data:
                await process_chunk_callback(chunk, chunk_data)

            # Wait between chunks
            await asyncio.sleep(random.uniform(2, 5))

        if failed_items:
            print(f"\n⚠️ 再取得が必要なアイテム: {len(failed_items)}件", flush=True)
            print(failed_items, flush=True)

    return results


def process_and_display_items(chunk_items, chunk_data_df, cutoff_date):
    """
    Process and display profit analysis for a chunk of items.

    Args:
        chunk_items (list): List of item IDs in this chunk
        chunk_data_df (pd.DataFrame): DataFrame with market data for this chunk
        cutoff_date (datetime): Cutoff date for filtering old data

    Returns:
        list: List of item analysis results
    """
    item_averages = []

    for item in chunk_items:
        item_data = chunk_data_df[chunk_data_df['item_id'] == item]

        # Calculate cost
        cost = calculate_cost(item)

        if len(item_data) > 0:
            # Calculate trade-count weighted average price
            total_value = (item_data['avg_price'] * item_data['item_count']).sum()
            total_count = item_data['item_count'].sum()

            if total_count > 0:
                weighted_avg_price = total_value / total_count
                latest_update = item_data['latest_timestamp'].max()

                # Calculate profit
                profit = (weighted_avg_price - cost) if cost is not None else None
                profit_pct = (profit / cost * 100) if profit is not None and cost > 0 else None

                # Extract Tier and Enchant
                parts = item.split("_", 1)
                tier = parts[0] if len(parts) > 0 else ""

                if len(parts) > 1 and "@" in parts[1]:
                    enchant = "@" + parts[1].split("@", 1)[1]
                else:
                    enchant = ""

                item_averages.append({
                    'item_id': item,
                    'cost': cost,
                    'tier': tier,
                    'enchant': enchant,
                    'weighted_avg_price': weighted_avg_price,
                    'profit': profit,
                    'profit_pct': profit_pct,
                    'total_trade_count': total_count,
                    'latest_update': latest_update
                })

    # Return results without displaying
    return item_averages


async def main():
    """
    Main execution function.
    Fetches market data, calculates costs and profits, and exports to CSV.
    """

    # Generate target items from configuration
    target_items = generate_all_items(ALL_ITEM_NAMES, DEFAULT_TIERS, DEFAULT_ENCHANTS)

    # Prepare cutoff date for filtering
    cutoff_date = datetime.now() - pd.Timedelta(days=7)

    # Storage for all results
    all_item_averages = []

    # Callback function to process each chunk
    async def process_chunk(chunk_items, chunk_data):
        if not chunk_data:
            return

        # Convert to DataFrame
        chunk_df = pd.DataFrame(chunk_data)
        chunk_df['latest_timestamp'] = pd.to_datetime(chunk_df['latest_timestamp'])

        # Filter to last 7 days
        chunk_df = chunk_df[chunk_df['latest_timestamp'] >= cutoff_date]

        if len(chunk_df) > 0:
            # Process and display chunk results
            chunk_results = process_and_display_items(chunk_items, chunk_df, cutoff_date)
            all_item_averages.extend(chunk_results)

    # Fetch data with chunk processing
    raw_data = await get_latest_timeseries_data(target_items, time_scale=6, process_chunk_callback=process_chunk)

    if not raw_data:
        print("❌ データが取得できませんでした", flush=True)
        return

    # Create final summary
    print(f"\n📊 最終集計結果:", flush=True)
    print(f"   取得データ総数: {len(raw_data)}件", flush=True)

    # Display final sorted results
    if all_item_averages:
        result_df = pd.DataFrame(all_item_averages)

        # Select and order columns
        output_columns = ['item_id', 'tier', 'enchant', 'cost', 'weighted_avg_price', 'profit', 'profit_pct', 'total_trade_count', 'latest_update']
        result_df = result_df[output_columns]

        # Rename columns for output
        result_df = result_df.rename(columns={
            'weighted_avg_price': 'avg_price',
            'total_trade_count': 'trade_count'
        })

        # Sort by profit percentage (highest first)
        result_df = result_df.sort_values('profit_pct', ascending=False)

        # Export to CSV
        output_file = "item_profit_analysis_7days.csv"
        result_df.to_csv(output_file, index=False)

        print(f"\n📈 全アイテム利益ランキング (上位10件):", flush=True)
        print(result_df.head(10).to_string(index=False), flush=True)
        print(f"\n✅ 完全な結果を {output_file} に出力しました", flush=True)

    else:
        print("❌ 有効な重み付け平均を計算できませんでした", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
