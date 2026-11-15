// Starter code generated with Claude (Anthropic); modified by Aashira
// Reads hit timestamps (ms), one per line. Prints: BPM steadiness(0-100)
#include <stdio.h>
#include <math.h>
#define MAX 100000
int main(void)
{
    static double t[MAX];
    int n = 0;
    while (n < MAX && scanf("%lf", &t[n]) == 1) n++;
    if (n < 3) { printf("0 0\n"); return 0; }
    double sum = 0, sq = 0;
    for (int i = 1; i < n; i++) sum += t[i] - t[i - 1];
    double mean = sum / (n - 1);
    for (int i = 1; i < n; i++) { double d = t[i] - t[i - 1] - mean; sq += d * d; }
    double sd = sqrt(sq / (n - 1));
    double steady = 100.0 * (1.0 - sd / mean);
    if (steady < 0) steady = 0;
    printf("%.1f %.1f\n", 60000.0 / mean, steady);
    return 0;
}
