
import ast
import importlib.util
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

# Import NetworkX for graph representation
import networkx as nx
import rich_click as click
from rich.console import Console
from typing_extensions import TypedDict

console = Console()

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent  # Reference to the parent node
        self.children = {}
        self.imports = []
        self.contents = {
            'functions': {},
            'classes': {},
            # Optional fields: 'docs', 'signatures', 'code', 'stats', 'info'
        }
        self.importance = 1.0  # Initial importance score

    def to_graph(self, G=None):
        """Recursively adds nodes and edges to a NetworkX graph.
        """
        if G is None:
            G = nx.DiGraph()
        G.add_node(self.name)
        for imp in self.imports:
            G.add_edge(self.name, imp)
        for child in self.children.values():
            child.to_graph(G)
        return G


def extract_node_info(file_path, include_docs=False, include_signatures=False, include_code=False):
    """
    Extracts imports, function definitions, class definitions,
    docstrings, and signatures from a Python file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    try:
        tree = ast.parse(source_code)
    except (SyntaxError, UnicodeDecodeError):
        return None  # Skip files that can't be parsed

    imports = []
    functions = {}
    classes = {}
    node_contents = {
        'imports': imports,
        'functions': functions,
        'classes': classes,
    }

    if include_docs:
        module_doc = ast.get_docstring(tree)
        if module_doc:
            node_contents['docs'] = module_doc

    signatures = {}

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ""
            imports.append(module)
        elif isinstance(node, ast.FunctionDef):
            func_name = node.name
            func_doc = ast.get_docstring(node) if include_docs else None
            args = [arg.arg for arg in node.args.args]
            functions[func_name] = {
                'docs': func_doc if include_docs else None,
                'args': args,
                # 'code' is optional
            }
            if include_signatures:
                signatures[func_name] = f"{func_name}({', '.join(args)})"
        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            class_doc = ast.get_docstring(node) if include_docs else None
            methods = {}
            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef):
                    method_name = body_item.name
                    method_doc = ast.get_docstring(body_item) if include_docs else None
                    args = [arg.arg for arg in body_item.args.args]
                    methods[method_name] = {
                        'docs': method_doc if include_docs else None,
                        'args': args,
                        # 'code' is optional
                    }
                    if include_signatures:
                        signatures[method_name] = f"{method_name}({', '.join(args)})"
            classes[class_name] = {
                'docs': class_doc if include_docs else None,
                'methods': methods,
                # 'code' is optional
            }

    if include_signatures and signatures:
        node_contents['signatures'] = signatures

    if include_code:
        node_contents['code'] = source_code

    return node_contents

def attempt_import(module_name):
    """Attempts to import a module by name. Returns True if successful, False otherwise."""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ModuleNotFoundError, ValueError):
        return False

class GraphDict(TypedDict):
    root_node: Node
    module_nodes: dict[str, Node]
    adjacency_list: dict[str, set[str]]
    reverse_adjacency_list: dict[str, set[str]]
    broken_imports: dict[str, set[str]]
    graph: nx.DiGraph
class Graph(NamedTuple):
    root_node: Node
    module_nodes: dict[str, Node]
    adjacency_list: dict[str, set[str]]
    reverse_adjacency_list: dict[str, set[str]]
    broken_imports: dict[str, set[str]]
    graph: nx.DiGraph
    
    def asdict(self) -> GraphDict:
        return {
            'root_node': self.root_node,
            'module_nodes': self.module_nodes,
            'adjacency_list': self.adjacency_list,
            'reverse_adjacency_list': self.reverse_adjacency_list,
            'broken_imports': self.broken_imports,
            'graph': self.graph,
        }
    

    
def build_dependency_graph(
    directory_path: Path | str,
    include_site_packages: bool = False,
    include_docs: bool = False,
    include_signatures: bool = False,
    include_code: bool = False,
)-> Graph:
    directory_path = Path(directory_path)
    directory_path = directory_path.parent.resolve() if directory_path.is_file() else directory_path.resolve()

    root_node = Node('root')
    module_nodes = {'root': root_node}
    adjacency_list = defaultdict(set)
    reverse_adjacency_list = defaultdict(set)  # For getting modules that import a given module
    broken_imports = defaultdict(set)  # Map broken imports to sets of file paths

    for file_path in directory_path.rglob('*.py'):
        # Skip site-packages and vendor directories if not included
        if not include_site_packages and (("site-packages" in file_path.parts) or ("vendor" in file_path.parts)):
            continue
        try:
            # Compute module's import path
            relative_path = file_path.relative_to(directory_path)
            parts = relative_path.with_suffix('').parts  # Remove '.py' suffix
            module_name = '.'.join(parts)
            parent_module_name = '.'.join(parts[:-1]) if len(parts) > 1 else 'root'
            parent_node = module_nodes.get(parent_module_name, root_node)

            # Extract node information
            node_info = extract_node_info(
                file_path,
                include_docs=include_docs,
                include_signatures=include_signatures,
                include_code=include_code,
            )
            if node_info is None:
                continue  # Skip files that couldn't be parsed

            # Create or get the module node
            module_node = Node(module_name, parent=parent_node)
            module_node.imports = node_info.get('imports', [])
            module_node.contents['functions'] = node_info.get('functions', {})
            module_node.contents['classes'] = node_info.get('classes', {})
            # Include optional fields if they exist
            if include_docs and 'docs' in node_info:
                module_node.contents['docs'] = node_info['docs']
            if include_signatures and 'signatures' in node_info:
                module_node.contents['signatures'] = node_info['signatures']
            if include_code and 'code' in node_info:
                module_node.contents['code'] = node_info['code']

            module_nodes[module_name] = module_node

            # Add to parent's children
            parent_node.children[module_name] = module_node

            # Update adjacency list for PageRank
            for imp in module_node.imports:
                adjacency_list[module_name].add(imp)
                reverse_adjacency_list[imp].add(module_name)
                # Initialize the importance of imported modules if not already
                if imp not in module_nodes:
                    module_nodes[imp] = Node(imp)
                # Update importance
                module_nodes[imp].importance += module_node.importance / max(len(module_node.imports), 1)

                # Attempt to import the module
                if not attempt_import(imp):
                    # Add the file path to the broken import's set
                    broken_imports[imp].add(str(file_path))

        except (SyntaxError, UnicodeDecodeError, ValueError):
            continue
    return Graph(**{
        'root_node': root_node,
        'module_nodes': module_nodes,
        'adjacency_list': adjacency_list,
        'reverse_adjacency_list': reverse_adjacency_list,
        'broken_imports': broken_imports,
        'graph': root_node.to_graph(),
    })

def print_tree(node, level=0, include_docs=False, include_signatures=False, include_code=False):
    indent = '  ' * level
    console.print(f"{indent}[bold light_goldenrod2]{node.name}[/bold light_goldenrod2]:")
    if node.imports:
        console.print(f"{indent}  Imports: {node.imports}")
    if node.contents.get('functions') or node.contents.get('classes'):
        console.print(f"{indent}  Contents:")
        for func_name, func_info in node.contents.get('functions', {}).items():
            console.print(f"{indent}    Function: {func_name}")
            if include_signatures:
                signature = node.contents.get('signatures', {}).get(func_name, '')
                if signature:
                    console.print(f"{indent}      Signature: {signature}")
            if include_docs and func_info.get('docs'):
                console.print(f"{indent}      Docstring: {func_info['docs']}")
        for class_name, class_info in node.contents.get('classes', {}).items():
            console.print(f"{indent}    Class: {class_name}")
            if include_docs and class_info.get('docs'):
                console.print(f"{indent}      Docstring: {class_info['docs']}")
            for method_name, method_info in class_info.get('methods', {}).items():
                console.print(f"{indent}      Method: {method_name}")
                if include_signatures:
                    signature = node.contents.get('signatures', {}).get(method_name, '')
                    if signature:
                        console.print(f"{indent}        Signature: {signature}")
                if include_docs and method_info.get('docs'):
                    console.print(f"{indent}        Docstring: {method_info['docs']}")
    if include_code and node.contents.get('code'):
        console.print(f"{indent}  Code:\n{node.contents['code']}")
    for child_node in node.children.values():
        print_tree(
            child_node,
            level=level+1,
            include_docs=include_docs,
            include_signatures=include_signatures,
            include_code=include_code,
        )

class GraphStats(TypedDict):
    num_modules: int
    num_imports: int
    num_functions: int
    num_classes: int
    avg_degree: float
    scc: list[set[str]]
    importance_scores: dict[str, float]
    effective_size: dict[str, float]
    pagerank: dict[str, float]
    
def get_stats(root_node, module_nodes, adjacency_list) -> GraphStats:
    """Computes statistics for the dependency graph."""
    num_modules = len(module_nodes)
    num_imports = sum(len(node.imports) for node in module_nodes.values())
    num_functions = sum(len(node.contents.get('functions', {})) for node in module_nodes.values())
    num_classes = sum(len(node.contents.get('classes', {})) for node in module_nodes.values())
     # Apply PageRank to determine module importance
    importance_scores = {node_name: node.importance for node_name, node in module_nodes.items()}
    total_importance = sum(importance_scores.values())
    # Normalize the importance scores
    if total_importance > 0:
        importance_scores = {node: score / total_importance for node, score in importance_scores.items()}
    else:
        importance_scores = {node: 0 for node in importance_scores}


    # Calculate average degree
    G = nx.DiGraph()
    for node, imports in adjacency_list.items():
        for imp in imports:
            G.add_edge(node, imp)
    pg = nx.algorithms.link_analysis.pagerank_alg.pagerank(G)
    avg_degree = sum(dict(G.degree()).values()) / float(len(G)) if len(G) > 0 else 0

    pg = {k: round(v, 4) for k, v in pg.items()}
    avg_degree = round(avg_degree, 2)

   # Find strongly connected components and rank them by size  
    scc = list(nx.strongly_connected_components(G))  
    # Rank SCCs by number of nodes  
    scc = sorted(scc, key=lambda x: len(x), reverse=True)  
    sizes = nx.effective_size(G)
    sizes = {k: round(v, 4) for k, v in sizes.items()}
    # Prepare sizes dict with neighbor info  
    sizes_with_neighbors = {  
        node: {  
            "effective_size": sizes[node],  
            "neighbors": len(list(G.neighbors(node))),
            "pagerank": round(pg[node] * G.number_of_edges(), 4)
        }  
        for node in G.nodes()  
    }  
    console.print(f"\n[bold light_goldenrod2]Effective Size of the Graph:[/bold light_goldenrod2] {sizes}")
    return {
        'num_modules': num_modules,
        'num_imports': num_imports,
        'num_functions': num_functions,
        'num_classes': num_classes,
        'avg_degree': avg_degree,
        'importance_scores': importance_scores,
        'scc': scc,
        "size": sorted(sizes_with_neighbors.items(), key=lambda x: x[1]["effective_size"], reverse=True),
        "pagerank": sorted(pg.items(), key=lambda x: x[1], reverse=True)
    }
from rich.pretty import Pretty
def display_stats(stats: GraphStats, exclude: set[str] = set()) -> None:
    """Displays statistics for the dependency graph."""
    for key, value in stats.items():
        if key in exclude or key not in ("pagerank", "size"):
            continue
        console.print(f"{key}")
        console.print(Pretty(value))

    

    # Display average degree
    console.print(f"Average Degree: {stats['avg_degree']:.2f}")

    # Display strongly connected components
    console.print("\n[bold light_goldenrod2]Strongly Connected Components:[/bold light_goldenrod2]")
    for i, component in enumerate(stats['scc'], start=1):
        console.print(f"Component {i}: {component}")
    for node, importance in stats['importance_scores'].items():
        console.print(f"Importance of {node}: {importance:.2f}")
        
@click.group()
def cli():
    pass

@cli.command("repair")
@click.argument("path", default=".")
@click.option("--sigs", is_flag=True, help="Include function and method signatures")
@click.option("--docs", is_flag=True, help="Include docstrings in the output")
@click.option("--code", is_flag=True, help="Include source code of modules in the output")
@click.option("--who-imports", is_flag=True, help="Include modules that import each module")
@click.option("--stats", is_flag=True, help="Include statistics and flow information")
@click.option("--site-packages", is_flag=True, help="Include site-packages and vendor directories")
def main(
    path: str = ".",
    sigs: bool = False,
    docs: bool = False,
    code: bool = False,
    who_imports: bool = False,
    stats: bool = False,
    site_packages: bool = False,
):
    # Build dependency graph and adjacency list
    result = build_dependency_graph(
        path,
        include_site_packages=site_packages,
        include_docs=docs,
        include_signatures=sigs,
        include_code=code,
    )
    root_node, module_nodes, adjacency_list, reverse_adjacency_list, broken_imports = result

    # Print the graph
    console.print("[bold light_goldenrod2]Dependency Graph:[/bold light_goldenrod2]")
    print_tree(
        root_node,
        include_docs=docs,
        include_signatures=sigs,
        include_code=code,
    )

    # Display statistics if requested
    if stats:
       display_stats(get_stats(root_node, module_nodes, adjacency_list))
    # Display importers if requested
    if who_imports:
        console.print("\n[bold light_goldenrod2]Importers:[/bold light_goldenrod2]")
        for module_name in module_nodes:
            importers = reverse_adjacency_list.get(module_name, set())
            if importers:
                console.print(f"\nModule: {module_name}")
                console.print(f"  Imported by: {list(importers)}")

    # Display broken imports with file paths
    if broken_imports:
        console.print("\n[bold red]Broken Imports:[/bold red]")
        for imp, file_paths in broken_imports.items():
            console.print(f"\nModule: {imp}")
            for path in file_paths:
                console.print(f" - Imported by: {path}")

@cli.command("who-imports")
@click.argument("module_name")
@click.argument("path", default=".")
@click.option("--site-packages", is_flag=True, help="Include site-packages and vendor directories")
def who_imports_command(module_name, path, site_packages):
    # Build dependency graph and adjacency list
    result = build_dependency_graph(path, include_site_packages=site_packages)
    root_node, module_nodes, adjacency_list, reverse_adjacency_list, broken_imports = result

    # Get modules that import the given module
    importers = reverse_adjacency_list.get(module_name, set())
    if importers:
        console.print(f"\n[bold light_goldenrod2]Modules that import '{module_name}':[/bold light_goldenrod2]")
        for importer in importers:
            console.print(f" - {importer}")
    else:
        console.print(f"\n[bold red]No modules found that import '{module_name}'.[/bold red]")

if __name__ == "__main__":
    sys.exit(cli())
