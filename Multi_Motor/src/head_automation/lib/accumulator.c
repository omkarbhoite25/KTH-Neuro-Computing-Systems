/**
 * accumulator.c -- C accelerator for event camera decay-weighted accumulator.
 *
 * Provides a fast path for the hot loop in event_tracking_node.py:
 *   1. Apply exponential decay to the entire accumulator
 *   2. Add incoming events to their (x, y) positions
 *   3. Compute weighted centroid
 *
 * Compile: gcc -O3 -shared -fPIC -o libaccumulator.so accumulator.c -lm
 *
 * Called from Python via ctypes.
 */

#include <math.h>
#include <stdint.h>

/**
 * Decay the accumulator and add new events.
 *
 * @param acc       Pointer to accumulator array (height x width, row-major float64)
 * @param width     Accumulator width (e.g. 128)
 * @param height    Accumulator height (e.g. 128)
 * @param ev_x      Array of event X coordinates (int32)
 * @param ev_y      Array of event Y coordinates (int32)
 * @param n_events  Number of events
 * @param decay     Decay factor (exp(-dt/tau)), applied to entire accumulator
 */
void accumulator_update(double *acc, int width, int height,
                        const int32_t *ev_x, const int32_t *ev_y,
                        int n_events, double decay)
{
    /* Validate dimensions to prevent integer overflow */
    if (width <= 0 || height <= 0 || width > 4096 || height > 4096) return;
    if (acc == NULL) return;

    /* Clamp decay to valid range */
    if (decay < 0.0) decay = 0.0;
    if (decay > 1.0) decay = 1.0;

    int size = width * height;

    /* Apply decay to entire accumulator */
    for (int i = 0; i < size; i++) {
        acc[i] *= decay;
    }

    /* Add events */
    for (int i = 0; i < n_events; i++) {
        int x = ev_x[i];
        int y = ev_y[i];
        if (x >= 0 && x < width && y >= 0 && y < height) {
            acc[y * width + x] += 1.0;
        }
    }
}

/**
 * Compute weighted centroid of the accumulator.
 *
 * @param acc     Pointer to accumulator array (height x width, row-major float64)
 * @param width   Accumulator width
 * @param height  Accumulator height
 * @param cx      Output: centroid X coordinate
 * @param cy      Output: centroid Y coordinate
 * @return        Total weight (sum of accumulator). If < epsilon, centroid is center.
 */
double accumulator_centroid(const double *acc, int width, int height,
                            double *cx, double *cy)
{
    if (width <= 0 || height <= 0 || width > 4096 || height > 4096 ||
        acc == NULL || cx == NULL || cy == NULL) {
        if (cx) *cx = 0.0;
        if (cy) *cy = 0.0;
        return 0.0;
    }

    double total = 0.0;
    double sum_x = 0.0;
    double sum_y = 0.0;

    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            double val = acc[y * width + x];
            total += val;
            sum_x += x * val;
            sum_y += y * val;
        }
    }

    if (total < 1e-6) {
        *cx = width / 2.0;
        *cy = height / 2.0;
    } else {
        *cx = sum_x / total;
        *cy = sum_y / total;
    }

    return total;
}
