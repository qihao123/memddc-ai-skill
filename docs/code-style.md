# 代码风格指南

## 1. 通用规则

### 1.1 缩进和空格
- 使用 2 个空格进行缩进
- 不使用制表符
- 行尾不保留空格
- 文件末尾保留一个空行

### 1.2 命名约定
- **变量名**：使用驼峰命名法（camelCase）
- **函数名**：使用驼峰命名法（camelCase）
- **类名**：使用帕斯卡命名法（PascalCase）
- **常量**：使用全大写字母，下划线分隔（UPPER_CASE_WITH_UNDERSCORES）
- **文件名**：使用小写字母，连字符分隔（kebab-case）
- **目录名**：使用小写字母，连字符分隔（kebab-case）

### 1.3 注释
- 代码注释使用 // 或 /* */
- 函数和类使用 JSDoc 风格注释
- 注释应简洁明了，解释代码的目的和逻辑
- 避免冗余注释，代码本身应该清晰易懂

### 1.4 代码长度
- 每行代码不超过 80 个字符
- 函数长度不超过 50 行
- 文件长度不超过 500 行

### 1.5 空行
- 函数之间使用两个空行
- 代码块之间使用一个空行
- 逻辑分组之间使用一个空行

## 2. 语言特定规则

### 2.1 JavaScript/TypeScript
- 使用单引号 `'` 而非双引号 `"`
- 使用箭头函数 `() => {}` 而非传统函数表达式
- 使用 `const` 和 `let`，避免使用 `var`
- 导入语句按字母顺序排序
- 导出语句放在文件末尾

#### 示例
```javascript
// 好的做法
const calculateTotal = (items) => {
  return items.reduce((total, item) => total + item.price, 0);
};

// 避免的做法
var calculate_total = function(items) {
  var total = 0;
  for (var i = 0; i < items.length; i++) {
    total += items[i].price;
  }
  return total;
};
```

### 2.2 Python
- 使用 4 个空格进行缩进
- 类名使用帕斯卡命名法（PascalCase）
- 函数和变量使用蛇形命名法（snake_case）
- 导入语句按标准库、第三方库、本地库的顺序分组
- 使用 docstring 为模块、函数和类添加文档

#### 示例
```python
# 好的做法
def calculate_total(items):
    """计算商品总价"""
    return sum(item.price for item in items)

class ShoppingCart:
    """购物车类"""
    def __init__(self):
        self.items = []
```

### 2.3 Java
- 使用 4 个空格进行缩进
- 类名使用帕斯卡命名法（PascalCase）
- 方法和变量使用驼峰命名法（camelCase）
- 包名使用小写字母
- 大括号 `{` 放在行尾，不单独占一行

#### 示例
```java
// 好的做法
public class ShoppingCart {
    private List<Item> items;
    
    public ShoppingCart() {
        this.items = new ArrayList<>();
    }
    
    public double calculateTotal() {
        return items.stream()
            .mapToDouble(Item::getPrice)
            .sum();
    }
}
```

### 2.4 Markdown
- 标题使用 `#` 符号，层次分明
- 代码块使用三个反引号 `\`\`\`` 包裹
- 列表使用 `-` 或 `*` 符号
- 链接使用 `[文本](URL)` 格式
- 图片使用 `![alt](URL)` 格式

#### 示例
```markdown
# 标题

## 子标题

- 列表项 1
- 列表项 2

```javascript
// 代码块
console.log('Hello, world!');
```

[链接文本](https://example.com)

![图片描述](https://example.com/image.jpg)
```

## 3. 架构特定规则

### 3.1 DDD 领域模型
- 实体类名使用帕斯卡命名法（PascalCase）
- 值对象类名使用帕斯卡命名法（PascalCase）
- 聚合根类名使用帕斯卡命名法（PascalCase）
- 领域服务类名使用帕斯卡命名法（PascalCase）
- 仓储接口名使用 `I` 前缀 + 帕斯卡命名法（IPascalCase）

### 3.2 目录结构
- 按功能模块组织目录
- 每个模块包含自己的实体、服务、仓储等
- 测试文件与源码文件放在同一目录，使用 `.test` 或 `.spec` 后缀
- 配置文件放在 `config` 目录
- 资源文件放在 `resources` 目录

## 4. 工具和配置

### 4.1 代码风格检查工具
- **JavaScript/TypeScript**：ESLint + Prettier
- **Python**：Flake8 + Black
- **Java**：Checkstyle + Spotless
- **Markdown**：markdownlint

### 4.2 配置文件示例

#### ESLint 配置
```json
{
  "extends": [
    "eslint:recommended",
    "prettier"
  ],
  "rules": {
    "indent": ["error", 2],
    "linebreak-style": ["error", "unix"],
    "quotes": ["error", "single"],
    "semi": ["error", "always"]
  }
}
```

#### Prettier 配置
```json
{
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 80,
  "tabWidth": 2
}
```

## 5. 代码审查

### 5.1 审查标准
- 代码是否符合风格指南
- 代码是否清晰易懂
- 代码是否符合 DDD 原则
- 代码是否有潜在的性能问题
- 代码是否有安全隐患

### 5.2 审查流程
1. 开发者提交代码前自查
2. 代码审查工具自动检查
3. 团队成员人工审查
4. 修复发现的问题
5. 合并代码

## 6. 版本控制

### 6.1 提交信息
- 提交信息应清晰明了
- 提交信息应包含：
  - 类型：feat（新功能）、fix（修复）、docs（文档）、style（代码风格）、refactor（重构）、test（测试）、chore（构建/依赖）
  - 范围：影响的模块
  - 描述：简要说明修改内容
- 示例：`feat(auth): add login functionality`

### 6.2 分支管理
- `main`：主分支，保持稳定
- `develop`：开发分支，集成新功能
- `feature/*`：特性分支，开发新功能
- `bugfix/*`：修复分支，修复bug
- `release/*`：发布分支，准备发布

## 7. 最佳实践

### 7.1 代码组织
- 遵循单一职责原则
- 保持函数和类的职责清晰
- 使用模块化设计
- 避免代码重复

### 7.2 性能优化
- 避免不必要的计算
- 使用适当的数据结构
- 优化循环和递归
- 合理使用缓存

### 7.3 安全性
- 避免硬编码敏感信息
- 输入验证
- 防止 SQL 注入
- 防止 XSS 攻击
- 安全的密码存储

### 7.4 可测试性
- 编写单元测试
- 使用依赖注入
- 避免紧耦合
- 模拟外部依赖

## 8. 常见问题

### 8.1 缩进不一致
- **问题**：代码缩进使用空格和制表符混合
- **解决方案**：统一使用 2 个或 4 个空格，根据语言选择

### 8.2 命名不规范
- **问题**：变量、函数、类命名不符合规范
- **解决方案**：遵循本指南的命名约定

### 8.3 代码过长
- **问题**：函数或文件过长，难以维护
- **解决方案**：拆分函数和文件，保持合理长度

### 8.4 注释不足
- **问题**：代码缺少必要的注释
- **解决方案**：为复杂逻辑和关键功能添加注释

### 8.5 风格不一致
- **问题**：团队成员代码风格不一致
- **解决方案**：使用代码风格检查工具，统一配置

## 9. 总结

代码风格指南的目的是：
1. 提高代码的可读性和可维护性
2. 减少代码审查的时间和成本
3. 促进团队协作和代码一致性
4. 降低错误率和调试时间

所有团队成员都应该遵守本指南，确保代码质量和一致性。