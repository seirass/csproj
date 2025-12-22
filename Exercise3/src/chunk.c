#include <merge.h>
#include <stdio.h>
#include "chunk.h"


CHUNK_Iterator CHUNK_CreateIterator(int fileDesc, int blocksInChunk) {
    CHUNK_Iterator it;
    it.file_desc = fileDesc;
    it.blocksInChunk = blocksInChunk;
    it.current = 1;  // ξεκινάμε από block 1
    it.lastBlocksID = HP_GetIdOfLastBlock(fileDesc);
    return it;
}

int CHUNK_GetNext(CHUNK_Iterator *iterator, CHUNK* chunk) {
    if (iterator->current > iterator->lastBlocksID)
        return -1;

    chunk->file_desc = iterator->file_desc;
    chunk->from_BlockId = iterator->current;

    int remaining = iterator->lastBlocksID - iterator->current + 1;
    chunk->blocksInChunk =
        remaining >= iterator->blocksInChunk ?
        iterator->blocksInChunk : remaining;

    chunk->to_BlockId = chunk->from_BlockId + chunk->blocksInChunk - 1;

    chunk->recordsInChunk = 0;
    for (int b = chunk->from_BlockId; b <= chunk->to_BlockId; b++) {
        chunk->recordsInChunk += HP_GetRecordCounter(chunk->file_desc, b);
    }

    iterator->current = chunk->to_BlockId + 1;
    return 0;
}

int CHUNK_GetIthRecordInChunk(CHUNK* chunk, int i, Record* record) {
    if (i < 0 || i >= chunk->recordsInChunk)
        return -1;

    int count = 0;

    for (int b = chunk->from_BlockId; b <= chunk->to_BlockId; b++) {
        int recs = HP_GetRecordCounter(chunk->file_desc, b);

        if (i < count + recs) {
            int cursor = i - count;
            HP_GetRecord(chunk->file_desc, b, cursor, record);
            HP_Unpin(chunk->file_desc, b);
            return 0;
        }
        count += recs;
    }
    return -1;
}

int CHUNK_UpdateIthRecord(CHUNK* chunk, int i, Record record) {
    if (i < 0 || i >= chunk->recordsInChunk)
        return -1;

    int count = 0;

    for (int b = chunk->from_BlockId; b <= chunk->to_BlockId; b++) {
        int recs = HP_GetRecordCounter(chunk->file_desc, b);

        if (i < count + recs) {
            int cursor = i - count;
            HP_UpdateRecord(chunk->file_desc, b, cursor, record);
            HP_Unpin(chunk->file_desc, b);
            return 0;
        }
        count += recs;
    }
    return -1;
}

void CHUNK_Print(CHUNK chunk) {
    for (int b = chunk.from_BlockId; b <= chunk.to_BlockId; b++) {
        HP_PrintBlockEntries(chunk.file_desc, b);
    }
}


CHUNK_RecordIterator CHUNK_CreateRecordIterator(CHUNK *chunk) {
    CHUNK_RecordIterator it;
    it.chunk = *chunk;
    it.currentBlockId = chunk->from_BlockId;
    it.cursor = 0;
    return it;
}

int CHUNK_GetNextRecord(CHUNK_RecordIterator *iterator, Record* record) {
    while (iterator->currentBlockId <= iterator->chunk.to_BlockId) {
        int recs = HP_GetRecordCounter(
            iterator->chunk.file_desc,
            iterator->currentBlockId
        );

        if (iterator->cursor < recs) {
            HP_GetRecord(
                iterator->chunk.file_desc,
                iterator->currentBlockId,
                iterator->cursor,
                record
            );
            HP_Unpin(iterator->chunk.file_desc, iterator->currentBlockId);
            iterator->cursor++;
            return 0;
        } else {
            iterator->currentBlockId++;
            iterator->cursor = 0;
        }
    }
    return -1;
}
