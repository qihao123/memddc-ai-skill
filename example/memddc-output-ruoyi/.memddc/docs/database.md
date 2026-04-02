# RuoYi-Vue 数据库设计文档

## 数据库概述

- **数据库类型**: MySQL
- **表数量**: 20张核心表
- **命名规范**: `sys_` 前缀表示系统表，`gen_` 前缀表示代码生成相关表
- **字符集**: UTF-8

## 数据表清单

### 系统管理表

| 表名 | 说明 | 核心字段 |
|------|------|---------|
| `sys_user` | 用户信息表 | user_id, dept_id, user_name, nick_name, password, email, phonenumber, sex, avatar, status, create_time |
| `sys_role` | 角色信息表 | role_id, role_name, role_key, role_sort, data_scope, status |
| `sys_menu` | 菜单权限表 | menu_id, menu_name, parent_id, order_num, path, component, icon, menu_type, status, perms |
| `sys_dept` | 部门表 | dept_id, parent_id, ancestors, dept_name, order_num, leader, phone, email, status |
| `sys_post` | 岗位表 | post_id, post_code, post_name, post_sort, status |
| `sys_dict_type` | 字典类型表 | dict_id, dict_name, dict_type, status |
| `sys_dict_data` | 字典数据表 | dict_code, dict_sort, dict_label, dict_value, dict_type, status |
| `sys_config` | 参数配置表 | config_id, config_name, config_key, config_value, config_type |
| `sys_notice` | 通知公告表 | notice_id, notice_title, notice_type, notice_content, status |
| `sys_notice_read` | 通知已读记录 | notice_id, user_id, read_time |

### 关联表

| 表名 | 说明 |
|------|------|
| `sys_user_role` | 用户-角色关联 |
| `sys_user_post` | 用户-岗位关联 |
| `sys_role_menu` | 角色-菜单关联 |
| `sys_role_dept` | 角色-部门关联（数据权限范围） |

### 监控/日志表

| 表名 | 说明 | 核心字段 |
|------|------|---------|
| `sys_logininfor` | 登录日志 | info_id, user_name, ipaddr, login_location, browser, os, status, msg, login_time |
| `sys_oper_log` | 操作日志 | oper_id, title, business_type, method, request_method, operator_type, oper_name, dept_name, oper_url, oper_ip, oper_location, oper_param, json_result, status, error_msg, oper_time |
| `sys_job` | 定时任务 | job_id, job_name, job_group, invoke_target, cron_expression, misfire_policy, concurrent, status |
| `sys_job_log` | 定时任务日志 | job_log_id, job_name, job_group, invoke_target, job_message, status, exception_info, create_time |

### 代码生成表

| 表名 | 说明 |
|------|------|
| `gen_table` | 代码生成业务表配置 |
| `gen_table_column` | 代码生成业务表字段配置 |

## 核心ER关系

```
sys_user (1) ──< (N) sys_user_role >── (N) sys_role (1)
sys_user (1) ──< (N) sys_user_post >── (N) sys_post
sys_role (1) ──< (N) sys_role_menu >── (N) sys_menu
sys_role (1) ──< (N) sys_role_dept >── (N) sys_dept
sys_dict_type (1) ──< (N) sys_dict_data
sys_notice (1) ──< (N) sys_notice_read >── (N) sys_user
sys_job (1) ──< (N) sys_job_log
```

## 树形结构表

- `sys_dept`: `parent_id` + `ancestors`（逗号分隔祖先路径）
- `sys_menu`: `parent_id` 自关联树

## 常用查询模式

1. **用户列表+部门名+角色**: 多表联查（`sys_user` LEFT JOIN `sys_dept`）
2. **菜单树**: 递归查询 `parent_id = 0` 逐级展开
3. **部门树**: 同样基于 `parent_id` 递归
4. **数据权限**: 在 `sys_user` 查询时动态拼接 `sys_dept` 范围条件
