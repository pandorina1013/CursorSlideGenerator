# Observer Pattern 実装

```javascript
momotaro.subscribe('enemy_detected', (enemy) => {
  team.members.forEach(member => 
    member.respondToThreat(enemy)
  );
});
```