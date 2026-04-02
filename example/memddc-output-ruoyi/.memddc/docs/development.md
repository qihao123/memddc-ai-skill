# 开发指南

## 1. 开发规范

### 命名规范
| 类型 | 规范 | 示例 |
|------|------|------|
| Controller | Sys{Entity}Controller | SysDeptController |
| Service | ISys{Entity}Service | ISysDeptService |
| ServiceImpl | Sys{Entity}ServiceImpl | SysDeptServiceImpl |
| Mapper | Sys{Entity}Mapper | SysDeptMapper |
| Entity | Sys{Entity} | SysDept |
| 表名 | sys_{entity} | sys_dept |

### API 规范
```java
// 查询列表
@GetMapping("/list")
public TableDataInfo list(Entity entity) {
    startPage();
    List<Entity> list = entityService.selectEntityList(entity);
    return getDataTable(list);
}

// 获取详情
@GetMapping("/{id}")
public AjaxResult getInfo(@PathVariable Long id) {
    return success(entityService.selectEntityById(id));
}

// 新增
@PostMapping
public AjaxResult add(@RequestBody Entity entity) {
    return toAjax(entityService.insertEntity(entity));
}

// 修改
@PutMapping
public AjaxResult edit(@RequestBody Entity entity) {
    return toAjax(entityService.updateEntity(entity));
}

// 删除
@DeleteMapping("/{ids}")
public AjaxResult remove(@PathVariable Long[] ids) {
    return toAjax(entityService.deleteEntityByIds(ids));
}
```

## 2. 新增功能步骤

### 后端
1. 设计数据库表
2. 生成代码（或使用代码生成器）
3. 调整实体类验证注解
4. 完善 Service 业务逻辑
5. 配置权限标识

### 前端
1. 在 views 下创建页面
2. 在 api 下定义接口
3. 配置路由
4. 配置菜单权限

## 3. 常用工具类

### SecurityUtils
```java
// 获取当前登录用户
LoginUser loginUser = SecurityUtils.getLoginUser();

// 判断是否管理员
boolean isAdmin = SecurityUtils.isAdmin(userId);
```

### StringUtils
```java
// 判断是否为空
StringUtils.isEmpty(str)
StringUtils.isNotEmpty(str)
StringUtils.isBlank(str)

// 分割字符串
StringUtils.split(str, ",")
```

### ServletUtils
```java
// 获取请求参数
String param = ServletUtils.getParameter("key");

// 渲染JSON响应
ServletUtils.renderString(response, json);
```

## 4. 数据权限

### 在 Service 层启用
```java
@DataScope(deptAlias = "d", userAlias = "u")
public List<SysUser> selectUserList(SysUser user) {
    return userMapper.selectUserList(user);
}
```

### 权限范围
- `1`: 全部数据权限
- `2`: 自定数据权限
- `3`: 本部门数据权限
- `4`: 本部门及以下数据权限
- `5`: 仅本人数据权限

## 5. 字典使用

### 前端
```vue
<!-- 字典下拉 -->
<dict-tag :options="dict.type.sys_normal_disable" :value="scope.row.status"/>

<!-- 字典选择 -->
<el-select v-model="form.status">
  <el-option
    v-for="dict in dict.type.sys_normal_disable"
    :key="dict.value"
    :label="dict.label"
    :value="dict.value"
  />
</el-select>
```

### 后端
```java
// Excel 导出时转换
@Excel(name = "状态", readConverterExp = "0=正常,1=停用")
private String status;
```

## 6. 定时任务

### 定义任务
```java
@Component("ryTask")
public class RyTask {
    public void ryParams(String params) {
        // 任务逻辑
    }
}
```

### 配置调用
- 调用方法: `ryTask.ryParams('params')`
- 支持 Cron 表达式

## 7. 常见问题

### 跨域问题
- 已在框架层统一处理
- 配置在 `application.yml`

### 事务控制
- 在 Service 层使用 `@Transactional`
- 默认回滚 RuntimeException

### 分页失效
- 确保 `startPage()` 在查询前调用
- 避免在分页查询后执行其他 SQL
