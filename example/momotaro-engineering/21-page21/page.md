# コードセクション

内容を追加してください。python
async def execute_attack():
    tasks = [
        dog_service.frontal_assault(),
        monkey_service.stealth_infiltration(),
        bird_service.aerial_support()
    ]
    results = await asyncio.gather(*tasks)
    return consolidate_victory(results)