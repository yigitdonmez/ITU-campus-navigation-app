#include <stdlib.h>
#include <string.h>
#include "graph.h"

Graph* create_graph(){
    Graph* graph = (Graph*)malloc(sizeof(Graph));
    graph->capacity = 0;
    graph->nodes = NULL;
    graph->num_nodes = 0;
    return graph;
}

void add_node(Graph* graph, int id, char* name, int x, int y){
    if (!graph) return;
    Node* newnode = (Node*)malloc(sizeof(Node));
    newnode->x = x;
    newnode->y = y;
    strncpy(newnode->name, name, sizeof(newnode->name));
    newnode->id = id;
    newnode->num_adj = 0;
    newnode->capacity = 0;
    newnode->adjacents = NULL;
    if(graph->capacity == graph->num_nodes) {
        graph->capacity = graph->capacity == 0 ? 4 : graph->capacity*2;
        Node** tempnodes = (Node**)malloc(graph->capacity*sizeof(Node*));
        for(int i = 0; i < graph->num_nodes; i++) {
            tempnodes[i] = graph->nodes[i];
        }
        free(graph->nodes);
        graph->nodes = tempnodes;
    }
    graph->nodes[graph->num_nodes++] = newnode;
}

void add_edge(Graph* graph, int sourceID, int destID, double weight){
    if(!graph) return;
    Edge* newedge = (Edge*)malloc(sizeof(Edge));
    newedge->dest = get_node_by_id(graph, destID);
    newedge->destID = destID;
    newedge->weight = weight;
    Node* srcnode = get_node_by_id(graph, sourceID);
    if(srcnode->capacity == srcnode->num_adj) {
        srcnode->capacity = srcnode->capacity == 0 ? 2 : 2*srcnode->capacity;
        Edge** tempedges = (Edge**)malloc(srcnode->capacity*sizeof(Edge*));
        for(int i = 0; i < srcnode->num_adj; i++) {
            tempedges[i] = srcnode->adjacents[i];
        }
        free(srcnode->adjacents);
        srcnode->adjacents = tempedges;
    }
    srcnode->adjacents[srcnode->num_adj++] = newedge;
}

Node* get_node_by_id(Graph* graph, int id) {
    if(!graph) return NULL;
    Node* node = NULL;
    for(int i = 0; i < graph->num_nodes; i++) {
        if(graph->nodes[i]->id == id) {
            node = graph->nodes[i];
            break;
        }
    }
    return node;
}

int get_node_index(Graph* graph, Node* node) {
    for (int i = 0; i < graph->num_nodes; i++) {
        if (graph->nodes[i] == node) return i;
    }
    return -1;
}

void delete_graph(Graph* graph) {
    if(!graph) return;
    for(int i = 0; i < graph->num_nodes; i++) {
        for(int j = 0; j < graph->nodes[i]->num_adj; j++) {
            free(graph->nodes[i]->adjacents[j]);
        }
        free(graph->nodes[i]->adjacents);
        free(graph->nodes[i]);
    }
    free(graph->nodes);
    free(graph);
}