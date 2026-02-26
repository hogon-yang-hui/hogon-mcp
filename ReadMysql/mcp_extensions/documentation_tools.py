"""MCP 文档生成工具 - 数据字典和 ER 图"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from mcp.server import Server

logger = logging.getLogger(__name__)

DocumentFormat = Literal["markdown", "html", "json"]


def register_documentation_tools(server: Server, db_ops: Any) -> None:
    """
    注册文档生成相关的 MCP Tools

    Args:
        server: MCP Server 实例
        db_ops: DatabaseOperations 实例
    """

    @server.tool()
    async def generate_data_dictionary(
        database: str,
        format: DocumentFormat = "markdown",
        include_sample_data: bool = False,
        output_filename: str | None = None
    ) -> dict[str, Any]:
        """
        生成数据字典文档

        Args:
            database: 数据库名称
            format: 输出格式（markdown/html/json）
            include_sample_data: 是否包含示例数据
            output_filename: 输出文件名（可选）

        Returns:
            生成结果信息
        """
        try:
            # 参数验证
            if format not in ("markdown", "html", "json"):
                return {
                    "success": False,
                    "error": f"不支持的格式: {format}，支持: markdown, html, json"
                }

            logger.info(f"开始生成数据字典: {database} (格式: {format})")

            # 获取数据库的所有表
            tables = await asyncio.to_thread(db_ops.list_tables, database)

            if not tables:
                return {
                    "success": False,
                    "error": f"数据库 {database} 中没有表"
                }

            # 收集所有表的详细信息
            tables_info = []
            total_tables = len(tables)

            for idx, table_name in enumerate(tables, 1):
                logger.info(f"  处理表 {idx}/{total_tables}: {table_name}")

                try:
                    table_info = await asyncio.to_thread(
                        db_ops.get_table_info, database, table_name
                    )

                    # 如果需要示例数据，查询前 3 行
                    sample_data = None
                    if include_sample_data:
                        try:
                            query = f"SELECT * FROM {table_name} LIMIT 3"
                            sample_result = await asyncio.to_thread(
                                db_ops.execute_query,
                                database,
                                query,
                                None,
                                3,
                                "generate_data_dictionary"
                            )
                            if sample_result.get("success"):
                                sample_data = sample_result.get("data", [])
                        except Exception as e:
                            logger.warning(f"  无法获取 {table_name} 的示例数据: {str(e)}")

                    tables_info.append({
                        "name": table_name,
                        "info": table_info,
                        "sample_data": sample_data
                    })

                except Exception as e:
                    logger.error(f"  获取表 {table_name} 信息失败: {str(e)}")
                    tables_info.append({
                        "name": table_name,
                        "error": str(e)
                    })

            # 生成文档
            if format == "markdown":
                content = _generate_markdown_dictionary(database, tables_info)
                extension = ".md"
            elif format == "html":
                content = _generate_html_dictionary(database, tables_info)
                extension = ".html"
            else:  # json
                content = json.dumps({
                    "database": database,
                    "generated_at": datetime.now().isoformat(),
                    "tables_count": len(tables_info),
                    "tables": tables_info
                }, ensure_ascii=False, indent=2, default=str)
                extension = ".json"

            # 生成文件名
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"data_dictionary_{database}_{timestamp}"

            # 移除扩展名（如果有）
            output_filename = Path(output_filename).stem

            # 保存文件
            output_dir = Path(__file__).parent.parent / "tmp" / "docs"
            output_dir.mkdir(parents=True, exist_ok=True)

            file_path = output_dir / f"{output_filename}{extension}"
            file_path.write_text(content, encoding='utf-8')

            file_size = file_path.stat().st_size

            logger.info(f"数据字典生成成功: {file_path} ({file_size} bytes)")

            return {
                "success": True,
                "database": database,
                "format": format,
                "tables_count": len(tables_info),
                "file_path": str(file_path),
                "file_size": file_size,
                "file_size_human": _format_size(file_size),
                "include_sample_data": include_sample_data
            }

        except Exception as e:
            logger.error(f"生成数据字典失败 [{database}]: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "database": database
            }

    @server.tool()
    async def generate_er_diagram(
        database: str,
        format: Literal["mermaid", "graphviz"] = "mermaid",
        include_fields: bool = True,
        output_filename: str | None = None
    ) -> dict[str, Any]:
        """
        生成 ER 图（实体关系图）

        Args:
            database: 数据库名称
            format: 输出格式（mermaid/graphviz）
            include_fields: 是否包含字段列表
            output_filename: 输出文件名（可选）

        Returns:
            生成结果信息
        """
        try:
            # 参数验证
            if format not in ("mermaid", "graphviz"):
                return {
                    "success": False,
                    "error": f"不支持的格式: {format}，支持: mermaid, graphviz"
                }

            logger.info(f"开始生成 ER 图: {database} (格式: {format})")

            # 获取数据库的所有表
            tables = await asyncio.to_thread(db_ops.list_tables, database)

            if not tables:
                return {
                    "success": False,
                    "error": f"数据库 {database} 中没有表"
                }

            # 收集所有表的结构信息
            tables_structure = []
            total_tables = len(tables)

            for idx, table_name in enumerate(tables, 1):
                logger.info(f"  处理表 {idx}/{total_tables}: {table_name}")

                try:
                    table_info = await asyncio.to_thread(
                        db_ops.get_table_info, database, table_name
                    )
                    tables_structure.append({
                        "name": table_name,
                        "fields": table_info.get("structure", []),
                        "row_count": table_info.get("row_count", 0)
                    })
                except Exception as e:
                    logger.error(f"  获取表 {table_name} 结构失败: {str(e)}")

            # 分析表之间的关系
            relationships = _analyze_relationships(tables_structure)

            # 生成 ER 图代码
            if format == "mermaid":
                content = _generate_mermaid_er(database, tables_structure, relationships, include_fields)
                extension = ".mmd"
            else:  # graphviz
                content = _generate_graphviz_er(database, tables_structure, relationships, include_fields)
                extension = ".dot"

            # 生成文件名
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"er_diagram_{database}_{timestamp}"

            # 移除扩展名（如果有）
            output_filename = Path(output_filename).stem

            # 保存文件
            output_dir = Path(__file__).parent.parent / "tmp" / "docs"
            output_dir.mkdir(parents=True, exist_ok=True)

            file_path = output_dir / f"{output_filename}{extension}"
            file_path.write_text(content, encoding='utf-8')

            file_size = file_path.stat().st_size

            # 同时生成一个带说明的 Markdown 文件
            if format == "mermaid":
                md_content = f"""# {database} 数据库 ER 图

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
表数量：{len(tables_structure)}
关系数量：{len(relationships)}

## ER 图

```mermaid
{content}
```

## 使用说明

此 ER 图使用 Mermaid 语法生成，可以：
1. 在支持 Mermaid 的 Markdown 编辑器中查看（如 VS Code、Typora）
2. 在 GitHub/GitLab 中直接渲染
3. 使用在线工具查看：https://mermaid.live/

## 表关系说明

{_format_relationships_description(relationships)}

---

原始 Mermaid 代码文件：{file_path.name}
"""
                md_path = output_dir / f"{output_filename}.md"
                md_path.write_text(md_content, encoding='utf-8')

                logger.info(f"ER 图生成成功: {file_path} 和 {md_path}")

                return {
                    "success": True,
                    "database": database,
                    "format": format,
                    "tables_count": len(tables_structure),
                    "relationships_count": len(relationships),
                    "file_path": str(file_path),
                    "markdown_path": str(md_path),
                    "file_size": file_size,
                    "file_size_human": _format_size(file_size),
                    "include_fields": include_fields
                }
            else:
                logger.info(f"ER 图生成成功: {file_path}")

                return {
                    "success": True,
                    "database": database,
                    "format": format,
                    "tables_count": len(tables_structure),
                    "relationships_count": len(relationships),
                    "file_path": str(file_path),
                    "file_size": file_size,
                    "file_size_human": _format_size(file_size),
                    "include_fields": include_fields
                }

        except Exception as e:
            logger.error(f"生成 ER 图失败 [{database}]: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "database": database
            }


def _generate_markdown_dictionary(database: str, tables_info: list[dict]) -> str:
    """生成 Markdown 格式的数据字典"""
    lines = [
        f"# {database} 数据库数据字典",
        "",
        f"**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**表数量：** {len(tables_info)}",
        "",
        "---",
        "",
        "## 目录",
        ""
    ]

    # 生成目录
    for idx, table in enumerate(tables_info, 1):
        if "error" not in table:
            table_name = table["name"]
            lines.append(f"{idx}. [{table_name}](#{table_name})")

    lines.extend(["", "---", ""])

    # 生成每个表的详细信息
    for table in tables_info:
        table_name = table["name"]

        if "error" in table:
            lines.extend([
                f"## {table_name}",
                "",
                f"**错误：** {table['error']}",
                "",
                "---",
                ""
            ])
            continue

        info = table["info"]
        structure = info.get("structure", [])
        row_count = info.get("row_count", 0)

        lines.extend([
            f"## {table_name}",
            "",
            f"**行数：** {row_count:,}",
            f"**字段数：** {len(structure)}",
            ""
        ])

        # 字段列表表格
        lines.extend([
            "### 字段列表",
            "",
            "| 字段名 | 类型 | 允许NULL | 键 | 默认值 | 额外 |",
            "|--------|------|----------|-----|--------|------|"
        ])

        for field in structure:
            field_name = field.get("Field", "")
            field_type = field.get("Type", "")
            null_flag = field.get("Null", "")
            key = field.get("Key", "")
            default = field.get("Default", "")
            extra = field.get("Extra", "")

            # 处理特殊字符
            default_str = str(default) if default is not None else ""

            lines.append(
                f"| {field_name} | {field_type} | {null_flag} | {key} | {default_str} | {extra} |"
            )

        # 示例数据
        if table.get("sample_data"):
            lines.extend([
                "",
                "### 示例数据",
                "",
                "```json",
                json.dumps(table["sample_data"], ensure_ascii=False, indent=2, default=str),
                "```"
            ])

        # CREATE 语句
        if info.get("create_statement"):
            lines.extend([
                "",
                "### 创建语句",
                "",
                "```sql",
                info["create_statement"],
                "```"
            ])

        lines.extend(["", "---", ""])

    return "\n".join(lines)


def _generate_html_dictionary(database: str, tables_info: list[dict]) -> str:
    """生成 HTML 格式的数据字典"""
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{database} 数据库数据字典</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #3498db;
            color: white;
            font-weight: 600;
        }}
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .meta {{
            color: #7f8c8d;
            margin: 10px 0;
        }}
        .key {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: bold;
        }}
        .key-pri {{
            background: #e74c3c;
            color: white;
        }}
        .key-uni {{
            background: #f39c12;
            color: white;
        }}
        .key-mul {{
            background: #3498db;
            color: white;
        }}
        code {{
            background: #ecf0f1;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{database} 数据库数据字典</h1>
        <div class="meta">
            <strong>生成时间：</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            <strong>表数量：</strong> {len(tables_info)}
        </div>
        <hr>
"""

    for table in tables_info:
        table_name = table["name"]

        if "error" in table:
            html += f"""
        <h2>{table_name}</h2>
        <p style="color: #e74c3c;"><strong>错误：</strong> {table['error']}</p>
        <hr>
"""
            continue

        info = table["info"]
        structure = info.get("structure", [])
        row_count = info.get("row_count", 0)

        html += f"""
        <h2 id="{table_name}">{table_name}</h2>
        <div class="meta">
            <strong>行数：</strong> {row_count:,} |
            <strong>字段数：</strong> {len(structure)}
        </div>

        <h3>字段列表</h3>
        <table>
            <thead>
                <tr>
                    <th>字段名</th>
                    <th>类型</th>
                    <th>允许NULL</th>
                    <th>键</th>
                    <th>默认值</th>
                    <th>额外</th>
                </tr>
            </thead>
            <tbody>
"""

        for field in structure:
            field_name = field.get("Field", "")
            field_type = field.get("Type", "")
            null_flag = field.get("Null", "")
            key = field.get("Key", "")
            default = field.get("Default", "")
            extra = field.get("Extra", "")

            # 处理键的显示
            key_html = ""
            if key == "PRI":
                key_html = '<span class="key key-pri">PRIMARY</span>'
            elif key == "UNI":
                key_html = '<span class="key key-uni">UNIQUE</span>'
            elif key == "MUL":
                key_html = '<span class="key key-mul">INDEX</span>'

            default_str = str(default) if default is not None else ""

            html += f"""
                <tr>
                    <td><code>{field_name}</code></td>
                    <td>{field_type}</td>
                    <td>{null_flag}</td>
                    <td>{key_html}</td>
                    <td>{default_str}</td>
                    <td>{extra}</td>
                </tr>
"""

        html += """
            </tbody>
        </table>
        <hr>
"""

    html += """
    </div>
</body>
</html>
"""

    return html


def _analyze_relationships(tables_structure: list[dict]) -> list[dict]:
    """分析表之间的关系（基于字段名推断）"""
    relationships = []

    for table in tables_structure:
        table_name = table["name"]
        fields = table.get("fields", [])

        for field in fields:
            field_name = field.get("Field", "")
            field_key = field.get("Key", "")

            # 检测外键模式：字段名以 _id 结尾，或包含其他表名
            if "_id" in field_name or "id" in field_name.lower():
                # 尝试推断关联的表
                potential_table = field_name.replace("_id", "").replace("_ID", "")

                # 检查是否存在这样的表
                for other_table in tables_structure:
                    other_table_name = other_table["name"]

                    # 简单的匹配规则
                    if (potential_table in other_table_name.lower() or
                        other_table_name.lower() in potential_table.lower()):

                        relationships.append({
                            "from_table": table_name,
                            "from_field": field_name,
                            "to_table": other_table_name,
                            "to_field": "id",  # 假设关联到主键
                            "type": "inferred"  # 推断的关系
                        })

    return relationships


def _generate_mermaid_er(database: str, tables_structure: list[dict],
                         relationships: list[dict], include_fields: bool) -> str:
    """生成 Mermaid ER 图代码"""
    lines = [
        "erDiagram"
    ]

    # 添加表定义
    for table in tables_structure:
        table_name = table["name"]
        fields = table.get("fields", [])

        if include_fields and fields:
            lines.append(f"    {table_name} {{")

            for field in fields[:10]:  # 限制最多10个字段，避免图太大
                field_name = field.get("Field", "")
                field_type = field.get("Type", "")
                field_key = field.get("Key", "")

                # 简化类型名称
                simple_type = field_type.split("(")[0]

                # 添加键标记
                key_mark = ""
                if field_key == "PRI":
                    key_mark = " PK"
                elif field_key == "UNI":
                    key_mark = " UK"
                elif field_key == "MUL":
                    key_mark = " FK"

                lines.append(f"        {simple_type} {field_name}{key_mark}")

            if len(fields) > 10:
                lines.append(f"        string ... (more {len(fields) - 10} fields)")

            lines.append("    }")

    # 添加关系
    for rel in relationships:
        from_table = rel["from_table"]
        to_table = rel["to_table"]

        # 使用 Mermaid 的关系语法
        lines.append(f"    {from_table} ||--o{{ {to_table} : has")

    return "\n".join(lines)


def _generate_graphviz_er(database: str, tables_structure: list[dict],
                          relationships: list[dict], include_fields: bool) -> str:
    """生成 GraphViz DOT 格式的 ER 图代码"""
    lines = [
        "digraph ER {",
        "    rankdir=LR;",
        "    node [shape=record, style=filled, fillcolor=lightblue];",
        ""
    ]

    # 添加表节点
    for table in tables_structure:
        table_name = table["name"]
        fields = table.get("fields", [])

        if include_fields and fields:
            field_lines = [f"<{table_name}> {table_name}"]

            for field in fields[:10]:  # 限制字段数
                field_name = field.get("Field", "")
                field_type = field.get("Type", "").split("(")[0]
                field_key = field.get("Key", "")

                key_mark = ""
                if field_key == "PRI":
                    key_mark = " 🔑"
                elif field_key == "UNI":
                    key_mark = " 🔐"

                field_lines.append(f"{field_name}: {field_type}{key_mark}")

            if len(fields) > 10:
                field_lines.append(f"... ({len(fields) - 10} more)")

            label = "|".join(field_lines)
            lines.append(f'    {table_name} [label="{label}"];')
        else:
            lines.append(f'    {table_name} [label="{table_name}"];')

    lines.append("")

    # 添加关系边
    for rel in relationships:
        from_table = rel["from_table"]
        to_table = rel["to_table"]
        lines.append(f'    {from_table} -> {to_table} [label="FK"];')

    lines.append("}")

    return "\n".join(lines)


def _format_relationships_description(relationships: list[dict]) -> str:
    """格式化关系描述"""
    if not relationships:
        return "未检测到表关系（基于字段名推断）"

    lines = []
    for idx, rel in enumerate(relationships, 1):
        lines.append(
            f"{idx}. `{rel['from_table']}.{rel['from_field']}` → "
            f"`{rel['to_table']}.{rel['to_field']}` (推断)"
        )

    return "\n".join(lines)


def _format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
