# Singleton Pattern 実装

```javascript
const KibidangoManager = (() => {
  let instance;
  return {
    getInstance: () => instance || (instance = new ResourceManager())
  };
})();
```