# RuoYi-Vue API接口文档

## 接口规范

- **基础URL**: `http://localhost:8080`
- **认证方式**: JWT Token（Header: `Authorization: Bearer {token}`）
- **响应格式**: JSON，统一包装为 `AjaxResult` / `R`
- **分页参数**: `pageNum`（当前页）, `pageSize`（每页大小）
- **分页响应**: `TableDataInfo { total, rows, code, msg }`

## Controller 列表（25个）

### 系统管理模块

| Controller | 功能说明 | 典型接口 |
|------------|---------|---------|
| `SysUserController` | 用户管理 | GET /system/user/list, POST /system/user, PUT /system/user, DELETE /system/user/{ids} |
| `SysRoleController` | 角色管理 | /system/role/** |
| `SysMenuController` | 菜单管理 | /system/menu/** |
| `SysDeptController` | 部门管理 | /system/dept/** |
| `SysPostController` | 岗位管理 | /system/post/** |
| `SysDictTypeController` | 字典类型 | /system/dict/type/** |
| `SysDictDataController` | 字典数据 | /system/dict/data/** |
| `SysConfigController` | 参数配置 | /system/config/** |
| `SysNoticeController` | 通知公告 | /system/notice/** |
| `SysProfileController` | 个人信息 | /system/user/profile/** |
| `SysRegisterController` | 用户注册 | /register |

### 系统监控模块

| Controller | 功能说明 | 典型接口 |
|------------|---------|---------|
| `SysUserOnlineController` | 在线用户 | /monitor/online/** |
| `SysJobController` | 定时任务 | /monitor/job/** |
| `SysJobLogController` | 定时任务日志 | /monitor/jobLog/** |
| `SysLogininforController` | 登录日志 | /monitor/logininfor/** |
| `SysOperlogController` | 操作日志 | /monitor/operlog/** |
| `ServerController` | 服务器监控 | /monitor/server |
| `CacheController` | 缓存监控 | /monitor/cache/** |

### 系统工具模块

| Controller | 功能说明 | 典型接口 |
|------------|---------|---------|
| `GenController` | 代码生成 | /tool/gen/** |

### 公共/认证模块

| Controller | 功能说明 | 典型接口 |
|------------|---------|---------|
| `SysLoginController` | 登录认证 | /login, /logout, /getInfo, /getRouters, /captchaImage |
| `CaptchaController` | 验证码 | /captchaImage |
| `CommonController` | 通用接口 | /common/download, /common/upload |
| `SysIndexController` | 首页/引导 | / |
| `TestController` | 测试接口 | /test/** |

## 前端 API 封装

前端在 `ruoyi-ui/src/api/` 目录下按模块封装：

```
api/
├── login.js          # 登录、注册、验证码、获取用户信息/路由
├── system/
│   ├── user.js
│   ├── role.js
│   ├── menu.js
│   ├── dept.js
│   ├── post.js
│   ├── dict/
│   │   ├── type.js
│   │   └── data.js
│   ├── config.js
│   └── notice.js
├── monitor/
│   ├── job.js
│   ├── jobLog.js
│   ├── logininfor.js
│   ├── operlog.js
│   ├── online.js
│   └── server.js
└── tool/
    ├── gen.js
    └── swagger.js
```

## 权限注解示例

```java
@PreAuthorize("@ss.hasPermi('system:user:list')")
@PreAuthorize("@ss.hasRole('admin')")
@DataScope(deptAlias = "d", userAlias = "u")
```
