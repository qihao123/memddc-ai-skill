# RuoYi-Vue Spring 技术栈文档

## Spring Boot 版本

- **Spring Boot**: 4.0.3
- **Java**: 17
- **Spring Security**: 集成 JWT 认证

## 关键 Starter

| Starter | 用途 |
|---------|------|
| `spring-boot-starter-web` | Web MVC |
| `spring-boot-starter-security` | 安全认证 |
| `spring-boot-starter-data-redis` | Redis缓存 |
| `mybatis-spring-boot-starter` | MyBatis集成 |
| `druid-spring-boot-4-starter` | 连接池监控 |
| `pagehelper-spring-boot-starter` | 分页插件 |
| `springdoc-openapi-starter-webmvc-ui` | API文档 |

## Spring Security 配置要点

- `SecurityConfig` 在 `ruoyi-framework` 中定义
- 配置链: 禁用 CSRF（前后端分离）、配置无状态Session、JWT过滤器、异常处理
- `JwtAuthenticationTokenFilter` 在每次请求时解析并验证 Token

## MyBatis 配置

- Mapper 扫描: `@MapperScan("com.ruoyi.**.mapper")`
- XML 位置: `classpath*:mapper/**/*.xml`
- 开启了 `mapUnderscoreToCamelCase`
- 分页插件 `PageHelper` 已自动配置

## AOP 切面

| 切面 | 类 | 功能 |
|------|-----|------|
| 日志切面 | `LogAspect` | 记录操作日志 |
| 数据权限 | `DataScopeAspect` | 动态拼接数据权限SQL |
| 防重提交 | `RepeatSubmitAspect` | 防止表单重复提交 |
| 限流 | `RateLimiterAspect` | 接口访问限流 |

## 异常处理

- `GlobalExceptionHandler` 统一处理控制器异常
- 返回 `AjaxResult.error(msg)` 标准化错误响应
