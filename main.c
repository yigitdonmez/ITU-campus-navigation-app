#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include "graph.h"

void load_nodes_from_file(Graph* graph, const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("Can not open file: %s\n", filename);
        return;
    }
    int id, x, y;
    char name[50];
    while (fscanf(file, "%d %s %d %d", &id, name, &x, &y) == 4) {
        add_node(graph, id, name, x, y);
    }
    fclose(file);
}

void load_edges_from_file(Graph* graph, const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        printf("Can not open file: %s\n", filename);
        return;
    }
    int src, dest;
    double weight;

    while (fscanf(file, "%d %d %lf", &src, &dest, &weight) == 3) {
        add_edge(graph, src, dest, weight);
        add_edge(graph, dest, src, weight);
    }
    fclose(file);
}

void find_shortest_path(Graph* graph, int start_id, int dest_id) {
    if (!graph) return;

    int* visited = (int*)malloc(graph->num_nodes*sizeof(int));
    for(int i = 0; i < graph->num_nodes; i++){
        visited[i] = 0;
        graph->nodes[i]->g_score = DBL_MAX;
        graph->nodes[i]->parent = NULL;
    }

    Node* startnode = get_node_by_id(graph, start_id);
    Node* endnode = get_node_by_id(graph, dest_id);

    if(!startnode || !endnode) {
        free(visited);
        return;
    }

    startnode->g_score = 0;

    for(int i = 0; i < graph->num_nodes; i++) {
        
        Node* current = NULL;
        double min_dist = DBL_MAX;
        int current_index = -1;
        for(int j = 0; j < graph->num_nodes; j++) {
            if(visited[j] == 0 && graph->nodes[j]->g_score < min_dist) {
                min_dist = graph->nodes[j]->g_score;
                current = graph->nodes[j];
                current_index = j;
            }
        }

        if (current == NULL || current->g_score == DBL_MAX) break;
        if (current->id == dest_id) break;

        visited[current_index] = 1;

        for(int j = 0; j < current->num_adj; j++) {
            Edge* edge = current->adjacents[j];
            Node* neighbor = edge->dest;
            int neighbor_index = get_node_index(graph, neighbor);
            if(visited[neighbor_index] == 0) {
                double new_dist = current->g_score + edge->weight;

                if(new_dist < neighbor->g_score) {
                    neighbor->g_score = new_dist;
                    neighbor->parent = current;
                }
            }
        }
    }
    free(visited);
}

void save_path_to_file(Graph* graph, int dest_id, const char* filename) {
    FILE* file = fopen(filename, "w");
    if (!file) return;

    Node* current = get_node_by_id(graph, dest_id);
    if(current->g_score == DBL_MAX) {
        fclose(file);
        return;
    }

    while (current != NULL) {
        fprintf(file, "%d %d %d\n", current->id, (int)current->x, (int)current->y);
        current = current->parent;
    }
    fclose(file);
    printf("Route saved to 'path.txt'.\n");
}

void save_path_info_to_file(Graph* itu_map, int dest_id, const char* filename) {
    Node* target = get_node_by_id(itu_map, dest_id);
    if (target != NULL) {
        FILE* finfo = fopen(filename, "w");
        if (finfo) {
            fprintf(finfo, "%.2f", target->g_score);
            fclose(finfo);
        }
    }
}

void print_path(Graph* graph, int dest_id) {
    Node* current = get_node_by_id(graph, dest_id);

    if(current->g_score == DBL_MAX) {
        printf("No way to this road!\n\n");
        return;
    }

    printf("\n=== SHORTEST PATH ===\n");
    printf("Total Distance: %.2f meters\n", current->g_score);
    printf("Estimated Time: %.1f minutes (On Foot)\n\n", current->g_score / 80.0);

    Node* path[1000];
    int count = 0;

    while (current != NULL) {
        path[count++] = current;
        current = current->parent;
    }

    for (int i = count - 1; i >= 0; i--) {
        printf("%d. %s", count - i, path[i]->name);
        if (path[i]->id >= 100) printf(" (Junction/Road)");
        printf("\n");
        if (i > 0) printf("    |\n    v\n");
    }
    printf("====================\n");
}

void print_locations(Graph* graph) {
    printf("ID   NAME\n");
    printf("====================\n");
    for(int i = 0; i < graph->num_nodes; i++) {
        Node* node = graph->nodes[i];
        if (node->id < 100) {
            printf("%-5d %s\n", node->id, node->name);
        }
    }
    printf("====================\n");

}


int main(int argc, char *argv[]) {
    Graph* itu_map = create_graph();

    load_nodes_from_file(itu_map, "nodes.txt");
    load_edges_from_file(itu_map, "edges_new.txt");

    if (argc == 3) {
        int startID = atoi(argv[1]);
        int endID = atoi(argv[2]);
        
        find_shortest_path(itu_map, startID, endID);
        save_path_to_file(itu_map, endID, "path.txt");
        save_path_info_to_file(itu_map, endID, "path_info.txt");
        
        delete_graph(itu_map);
        return 0;
    }

    //If not enough arguments taking inputs with console
    int startID, endID;

    while(1) {
        printf("\nEnter Start Node ID (-1 to Exit and 0 to See All Locations): ");
        scanf("%d", &startID);
        if (startID == -1) break;
        if (startID == 0) {
            print_locations(itu_map);
            continue;
        }

        printf("Destination Node ID: ");
        scanf("%d", &endID);

        find_shortest_path(itu_map, startID, endID);
        save_path_to_file(itu_map, endID, "path.txt");
        print_path(itu_map, endID);
    }

    delete_graph(itu_map);
    return 0;
}