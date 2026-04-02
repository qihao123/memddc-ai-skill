# RuoYi-Vue Java 类结构文档

## 核心实体类（在 ruoyi-common 中定义）

| 类名 | 路径 | 说明 |
|------|------|------|
| `SysUser` | `com.ruoyi.common.core.domain.entity` | 用户实体 |
| `SysRole` | `com.ruoyi.common.core.domain.entity` | 角色实体 |
| `SysMenu` | `com.ruoyi.common.core.domain.entity` | 菜单实体 |
| `SysDept` | `com.ruoyi.common.core.domain.entity` | 部门实体 |
| `SysDictType` | `com.ruoyi.common.core.domain.entity` | 字典类型 |
| `SysDictData` | `com.ruoyi.common.core.domain.entity` | 字典数据 |
| `BaseEntity` | `com.ruoyi.common.core.domain` | 基础实体（createBy, createTime, updateBy, updateTime, remark） |
| `TreeEntity` | `com.ruoyi.common.core.domain` | 树形基础实体（parentId, ancestors, orderNum） |
| `LoginUser` | `com.ruoyi.common.core.domain.model` | 登录用户模型 |
| `LoginBody` | `com.ruoyi.common.core.domain.model` | 登录请求体 |
| `RegisterBody` | `com.ruoyi.common.core.domain.model` | 注册请求体 |

## 核心控制器（在 ruoyi-admin 中）

- `SysUserController` - 用户管理
- `SysRoleController` - 角色管理
- `SysMenuController` - 菜单管理
- `SysDeptController` - 部门管理
- `SysLoginController` - 登录认证

## 核心服务（在 ruoyi-system 中）

- `ISysUserService` / `SysUserServiceImpl`
- `ISysRoleService` / `SysRoleServiceImpl`
- `ISysMenuService` / `SysMenuServiceImpl`
- `ISysDeptService` / `SysDeptServiceImpl`
- `SysLoginService` - 登录业务
- `TokenService` - Token生成与校验
- `PermissionService` - 权限校验辅助

## 工具类清单

| 类名 | 说明 |
|------|------|
| `RedisCache` | Redis操作封装 |
| `Convert` | 类型转换工具 |
| `ServletUtils` | Servlet工具 |
| `StringUtils` | 字符串工具 |
| `DateUtils` | 日期工具 |
| `JsonUtils` | JSON序列化 |
| `FileUtils` | 文件操作 |
| `ExcelUtil` | Excel导入导出 |
| `SecurityUtils` | 安全上下文获取 |
