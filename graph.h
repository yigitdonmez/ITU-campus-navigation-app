#ifndef GRAPH_H
#define GRAPH_H

typedef struct Node {
    char name[50];
    int id;
    double x, y;
    struct Edge** adjacents;
    int capacity;
    int num_adj;
    double g_score;
    struct Node* parent;
} Node;

typedef struct Edge {
    double weight;
    int destID;
    struct Node* dest;
} Edge;

typedef struct Graph {
    struct Node** nodes;
    int capacity;
    int num_nodes;
} Graph;

Graph* create_graph();
void add_node(Graph* graph, int id, char* name, int x, int y);
void add_edge(Graph* graph, int sourceID, int destID, double weight);
Node* get_node_by_id(Graph* graph, int id);
int get_node_index(Graph* graph, Node* node);
void delete_graph(Graph* graph);

#endif