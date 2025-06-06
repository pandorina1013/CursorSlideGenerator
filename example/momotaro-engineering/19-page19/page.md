# 偵察フェーズ

```python
async def reconnaissance():
    bird_data = await bird_service.scout_island()
    enemy_count = await analyze_threats(bird_data)
    return create_attack_plan(enemy_count)
```