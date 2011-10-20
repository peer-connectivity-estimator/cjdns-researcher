#ifndef NODE_STORE_H
#define NODE_STORE_H

#include <stdint.h>
#include <stdbool.h>

#include "memory/MemAllocator.h"

struct NodeStore;

/**
 * Create a new NodeStore.
 *
 * @param myAddress the address for this DHT node.
 * @param capacity the number of nodes which this store can hold.
 * @param allocator the allocator to allocate storage space for this NodeStore.
 */
struct NodeStore* NodeStore_new(const uint8_t myAddress[20],
                                const uint32_t capacity,
                                const struct MemAllocator* allocator);

/**
 * Find a node in the store.
 *
 * @param store a store to get the node from.
 * @param address the identifier for the node to lookup.
 * @return A pointer to the node if one is found, otherwise NULL.
 */
struct Node* NodeStore_getNode(const struct NodeStore* store, const uint8_t address[20]);

/**
 * Put a node into the store.
 *
 * @param store a node store to insert into.
 * @param address the address of the new node.
 * @param networkAddress the network address to get to the new node.
 */
void NodeStore_addNode(struct NodeStore* store,
                       const uint8_t address[20],
                       const uint8_t networkAddress[6]);

/**
 * Get the best nodes for servicing a lookup.
 * These are returned in reverse order, from farthest to closest.
 *
 * @param store the store to get the nodes from.
 * @param targetAddress the address to get the bast nodes for.
 * @param count the number of nodes to return.
 * @param allowNodesFartherThanUs if true then return nodes which are farther than the target then we are.
 *                                this is required for searches but unallowable for answering queries.
 * @param allocator the memory allocator to use for getting the memory to store the output.
 */
struct NodeList* NodeStore_getClosestNodes(struct NodeStore* store,
                                           const uint8_t targetAddress[20],
                                           const uint32_t count,
                                           const bool allowNodesFartherThanUs,
                                           const struct MemAllocator* allocator);

/**
 * Change the reach of a node in the NodeStore.
 * Just changing the reach number will have no effect unless it is "committed"
 * by calling NodeStore_updateReach().
 *
 * @param node the node to update.
 * @param store the store where that node is contained.
 */
void NodeStore_updateReach(struct Node* const node,
                           struct NodeStore* const store);
#endif
