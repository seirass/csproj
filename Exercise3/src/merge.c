#include <merge.h>
#include <stdio.h>
#include <stdbool.h>

void merge(int input_FileDesc, int chunkSize, int bWay, int output_FileDesc) {

    CHUNK_Iterator chunkIt =
        CHUNK_CreateIterator(input_FileDesc, chunkSize);

    while (1) {

        /* ---- Φόρτωση έως bWay chunks ---- */
        CHUNK chunks[bWay];
        CHUNK_RecordIterator recordIts[bWay];
        Record currentRecords[bWay];
        bool hasRecord[bWay];

        int chunksLoaded = 0;

        for (int i = 0; i < bWay; i++) {
            if (CHUNK_GetNext(&chunkIt, &chunks[i]) == 0) {
                recordIts[i] =
                    CHUNK_CreateRecordIterator(&chunks[i]);
                if (CHUNK_GetNextRecord(&recordIts[i],
                                        &currentRecords[i]) == 0) {
                    hasRecord[i] = true;
                } else {
                    hasRecord[i] = false;
                }
                chunksLoaded++;
            } else {
                break;
            }
        }

        if (chunksLoaded == 0)
            break;

        /* ---- Συγχώνευση των chunks ---- */
        while (1) {
            int minIndex = -1;

            for (int i = 0; i < chunksLoaded; i++) {
                if (!hasRecord[i])
                    continue;

                if (minIndex == -1 ||
                    shouldSwap(&currentRecords[minIndex],
                               &currentRecords[i])) {
                    minIndex = i;
                }
            }

            if (minIndex == -1)
                break;

            HP_InsertEntry(output_FileDesc,
                           currentRecords[minIndex]);

            if (CHUNK_GetNextRecord(&recordIts[minIndex],
                                    &currentRecords[minIndex]) == 0) {
                hasRecord[minIndex] = true;
            } else {
                hasRecord[minIndex] = false;
            }
        }
    }
}
