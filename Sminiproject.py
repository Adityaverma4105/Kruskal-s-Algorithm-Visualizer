import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import json
import heapq

class AdvancedKruskalGraph:
    def __init__(self):
        self.V = 0
        self.graph = []
        self.node_positions = {}
        self.create_gui()

    def add_edge(self, u, v, w):
        """Add edge to the graph"""
        self.graph.append([u, v, w])
        # Update vertex count
        self.V = max(self.V, u+1, v+1)

    def find(self, parent, i):
        """Find set of an element (uses path compression)"""
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        """Union of two sets (by rank)"""
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal_mst(self):
        """Kruskal's algorithm implementation"""
        if self.V == 0:
            return []
            
        result = []
        i, e = 0, 0
        # Sort edges by weight
        self.graph = sorted(self.graph, key=lambda item: item[2])
        parent = []
        rank = []
        
        # Initialize parent and rank arrays
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
            
        # Process edges until we have V-1 edges in MST
        while e < self.V - 1 and i < len(self.graph):
            u, v, w = self.graph[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            
            # If including this edge doesn't cause cycle, include it
            if x != y:
                e += 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
                
        return result

    def calculate_mst_weight(self, mst):
        """Calculate total weight of MST"""
        return sum(edge[2] for edge in mst)

    def visualize_graph(self, mst_edges=None):
        """Visualize the graph with matplotlib"""
        G = nx.Graph()
        
        # Add all nodes
        for i in range(self.V):
            G.add_node(i)
        
        # Add all edges
        for u, v, w in self.graph:
            G.add_edge(u, v, weight=w, color='black')
        
        # If MST edges provided, color them differently
        if mst_edges:
            for u, v, w in mst_edges:
                if G.has_edge(u, v):
                    G[u][v]['color'] = 'red'
                    G[u][v]['width'] = 3
        
        # Use predefined positions or generate them
        if not self.node_positions:
            pos = nx.spring_layout(G)
            self.node_positions = pos
        else:
            pos = self.node_positions
            
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Get edge colors and widths
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]
        edge_widths = [G[u][v].get('width', 1.5) for u, v in G.edges()]
        edge_labels = nx.get_edge_attributes(G, 'weight')
        
        # Draw graph
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold', ax=ax)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, ax=ax)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        
        ax.set_title("Graph Visualization")
        ax.axis('off')
        
        return fig

    def create_gui(self):
        """Create the main GUI"""
        self.root = tk.Tk()
        self.root.title("Advanced Kruskal's Algorithm Visualizer")
        self.root.geometry("1200x800")
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Advanced Kruskal's Algorithm Visualizer", 
                               font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Graph Controls", padding="10")
        controls_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Edge input controls
        ttk.Label(controls_frame, text="Node U:").grid(row=0, column=0, padx=(0, 5))
        self.node_u_var = tk.StringVar()
        ttk.Entry(controls_frame, textvariable=self.node_u_var, width=10).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(controls_frame, text="Node V:").grid(row=0, column=2, padx=(0, 5))
        self.node_v_var = tk.StringVar()
        ttk.Entry(controls_frame, textvariable=self.node_v_var, width=10).grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(controls_frame, text="Weight:").grid(row=0, column=4, padx=(0, 5))
        self.weight_var = tk.StringVar()
        ttk.Entry(controls_frame, textvariable=self.weight_var, width=10).grid(row=0, column=5, padx=(0, 10))
        
        add_btn = ttk.Button(controls_frame, text="Add Edge", command=self.add_edge_handler)
        add_btn.grid(row=0, column=6, padx=(0, 10))
        
        # Example graph buttons
        example_btn = ttk.Button(controls_frame, text="Load Example Graph", command=self.load_example_graph)
        example_btn.grid(row=0, column=7, padx=(0, 10))
        
        clear_btn = ttk.Button(controls_frame, text="Clear Graph", command=self.clear_graph)
        clear_btn.grid(row=0, column=8, padx=(0, 10))
        
        # Algorithm controls
        algo_frame = ttk.LabelFrame(main_frame, text="Algorithm Controls", padding="10")
        algo_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        algo_frame.columnconfigure(0, weight=1)
        
        run_btn = ttk.Button(algo_frame, text="Run Kruskal's Algorithm", command=self.run_kruskal)
        run_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Results text area
        self.result_text = tk.Text(algo_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(algo_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Visualization frame
        viz_frame = ttk.LabelFrame(main_frame, text="Graph Visualization", padding="10")
        viz_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10), padx=(10, 0))
        viz_frame.columnconfigure(0, weight=1)
        viz_frame.rowconfigure(0, weight=1)
        
        # Initial visualization
        self.fig = self.visualize_graph()
        self.canvas = FigureCanvasTkAgg(self.fig, master=viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Visualization controls
        viz_controls_frame = ttk.Frame(main_frame)
        viz_controls_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        refresh_btn = ttk.Button(viz_controls_frame, text="Refresh Visualization", command=self.refresh_visualization)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_btn = ttk.Button(viz_controls_frame, text="Save Graph Data", command=self.save_graph)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        load_btn = ttk.Button(viz_controls_frame, text="Load Graph Data", command=self.load_graph)
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Add edges to the graph")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def add_edge_handler(self):
        """Handle add edge button click"""
        try:
            u = int(self.node_u_var.get())
            v = int(self.node_v_var.get())
            w = float(self.weight_var.get())
            
            if u < 0 or v < 0:
                messagebox.showerror("Input Error", "Node values must be non-negative integers")
                return
                
            self.add_edge(u, v, w)
            self.status_var.set(f"Added edge ({u}, {v}) with weight {w}")
            messagebox.showinfo("Success", f"Edge ({u}, {v}) with weight {w} added successfully")
            
            # Clear input fields
            self.node_u_var.set("")
            self.node_v_var.set("")
            self.weight_var.set("")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for nodes and weight")

    def load_example_graph(self):
        """Load a predefined example graph"""
        self.clear_graph()
        
        # Example graph (similar to original but with more edges)
        example_edges = [
            (0, 1, 10), (0, 2, 6), (0, 3, 5),
            (1, 3, 15), (2, 3, 4), (1, 2, 8),
            (3, 4, 7), (2, 4, 3), (1, 4, 9)
        ]
        
        for u, v, w in example_edges:
            self.add_edge(u, v, w)
            
        self.status_var.set("Loaded example graph")
        self.refresh_visualization()
        messagebox.showinfo("Success", "Example graph loaded successfully")

    def clear_graph(self):
        """Clear the current graph"""
        self.V = 0
        self.graph = []
        self.node_positions = {}
        self.result_text.delete(1.0, tk.END)
        self.status_var.set("Graph cleared")
        self.refresh_visualization()

    def run_kruskal(self):
        """Run Kruskal's algorithm and display results"""
        if not self.graph:
            messagebox.showwarning("No Data", "Please add edges to the graph first")
            return
            
        try:
            mst = self.kruskal_mst()
            
            if not mst:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "No MST could be formed (graph may be disconnected)\n")
                self.status_var.set("No MST formed")
                self.refresh_visualization([])
                return
                
            total_weight = self.calculate_mst_weight(mst)
            
            # Display results
            result_str = f"Minimum Spanning Tree found with total weight: {total_weight}\n\n"
            result_str += "Edges in the MST:\n"
            for i, (u, v, w) in enumerate(mst):
                result_str += f"{i+1}. {u} -- {v} == {w}\n"
                
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_str)
            self.status_var.set(f"MST calculated with total weight {total_weight}")
            
            # Update visualization with MST edges highlighted
            self.refresh_visualization(mst)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while running Kruskal's algorithm: {str(e)}")

    def refresh_visualization(self, mst_edges=None):
        """Refresh the graph visualization"""
        # Clear the previous canvas
        self.canvas.get_tk_widget().destroy()
        
        # Create new figure
        self.fig = self.visualize_graph(mst_edges)
        canvas_frame = self.canvas.get_tk_widget().master
        self.canvas = FigureCanvasTkAgg(self.fig, master=canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def save_graph(self):
        """Save current graph to file"""
        if not self.graph:
            messagebox.showwarning("No Data", "No graph data to save")
            return
            
        try:
            data = {
                "vertices": self.V,
                "edges": self.graph,
                "positions": self.node_positions
            }
            
            with open("graph_data.json", "w") as f:
                json.dump(data, f)
                
            messagebox.showinfo("Success", "Graph data saved successfully")
            self.status_var.set("Graph data saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save graph data: {str(e)}")

    def load_graph(self):
        """Load graph from file"""
        try:
            with open("graph_data.json", "r") as f:
                data = json.load(f)
                
            self.V = data["vertices"]
            self.graph = data["edges"]
            self.node_positions = data.get("positions", {})
            
            self.result_text.delete(1.0, tk.END)
            self.status_var.set("Graph data loaded")
            self.refresh_visualization()
            messagebox.showinfo("Success", "Graph data loaded successfully")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved graph data found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load graph data: {str(e)}")

    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = AdvancedKruskalGraph()
    app.run()