#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bf.h"
#include "hp_file.h"
#include "record.h"
#include "sort.h"
#include "merge.h"
#include "chunk.h"

bool shouldSwap(Record* rec1, Record* rec2) {
    if (strcmp(rec1->name, rec2->name) > 0)
        return true;

    if (strcmp(rec1->name, rec2->name) == 0 &&
        strcmp(rec1->surname, rec2->surname) > 0)
        return true;

    return false;
}

void sort_Chunk(CHUNK* chunk) {
    Record r1, r2;

    for (int i = 0; i < chunk->recordsInChunk - 1; i++) {
        for (int j = 0; j < chunk->recordsInChunk - i - 1; j++) {

            CHUNK_GetIthRecordInChunk(chunk, j, &r1);
            CHUNK_GetIthRecordInChunk(chunk, j + 1, &r2);

            if (shouldSwap(&r1, &r2)) {
                CHUNK_UpdateIthRecord(chunk, j, r2);
                CHUNK_UpdateIthRecord(chunk, j + 1, r1);
            }
        }
    }
}

void sort_FileInChunks(int file_desc, int numBlocksInChunk) {

    CHUNK_Iterator it =
        CHUNK_CreateIterator(file_desc, numBlocksInChunk);

    CHUNK chunk;

    while (CHUNK_GetNext(&it, &chunk) == 0) {
        sort_Chunk(&chunk);
    }
}