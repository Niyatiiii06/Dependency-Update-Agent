import os
import ast


IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules"
}


def find_methods(tree, function_name):
    methods = []

    for node in ast.walk(tree):

        if isinstance(node, ast.ClassDef):

            for child in node.body:

                if isinstance(child, ast.FunctionDef):

                    if child.name == function_name:

                        methods.append({
                            "class": node.name,
                            "line": child.lineno
                        })

    return methods


def find_calls(tree, function_name):
    calls = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            current_function = node.name

            for child in ast.walk(node):

                if isinstance(child, ast.Call):

                    if isinstance(child.func, ast.Name):

                        if child.func.id == function_name:

                            calls.append({
                                "caller": current_function,
                                "line": child.lineno
                            })

                    elif isinstance(child.func, ast.Attribute):

                        if child.func.attr == function_name:

                            calls.append({
                                "caller": current_function,
                                "line": child.lineno
                            })

    return calls


def search_code(project_path, function_name):

    results = {
        "definitions": [],
        "calls": [],
        "imports": [],
        "called_by": []
    }

    for root, dirs, files in os.walk(project_path):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORED_DIRS
        ]

        for file in files:

            if not file.endswith(".py"):
                continue

            filepath = os.path.join(root, file)

            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()

            try:
                tree = ast.parse(code)

            except SyntaxError:
                continue

            methods = find_methods(tree, function_name)

            for method in methods:

                results["definitions"].append({
                    "file": filepath,
                    "line": method["line"],
                    "code": f"{method['class']}.{function_name}()"
                })

            calls = find_calls(tree, function_name)

            for call in calls:

                results["called_by"].append({
                    "file": filepath,
                    "line": call["line"],
                    "caller": call["caller"]
                })

            for node in ast.walk(tree):

                if isinstance(node, ast.FunctionDef):

                    parent_is_class = False

                    for parent in ast.walk(tree):

                        if isinstance(parent, ast.ClassDef):

                            if node in parent.body:

                                parent_is_class = True
                                break

                    if node.name == function_name and not parent_is_class:

                        results["definitions"].append({
                            "file": filepath,
                            "line": node.lineno,
                            "code": f"def {node.name}"
                        })

                elif isinstance(node, ast.Call):

                    if isinstance(node.func, ast.Name):

                        if node.func.id == function_name:

                            results["calls"].append({
                                "file": filepath,
                                "line": node.lineno,
                                "code": f"{node.func.id}()"
                            })

                    elif isinstance(node.func, ast.Attribute):

                        if node.func.attr == function_name:

                            if isinstance(node.func.value, ast.Name):

                                results["calls"].append({
                                    "file": filepath,
                                    "line": node.lineno,
                                    "code": (
                                        f"{node.func.value.id}."
                                        f"{node.func.attr}()"
                                    )
                                })

                elif isinstance(node, ast.Import):

                    for alias in node.names:

                        if alias.name == function_name:

                            results["imports"].append({
                                "file": filepath,
                                "line": node.lineno,
                                "code": f"import {alias.name}"
                            })

                elif isinstance(node, ast.ImportFrom):

                    for alias in node.names:

                        if alias.name == function_name:

                            results["imports"].append({
                                "file": filepath,
                                "line": node.lineno,
                                "code": (
                                    f"from {node.module} "
                                    f"import {alias.name}"
                                )
                            })

    return results