#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

// construct the sparse table
std::vector<std::vector<int>> sparseTable(const std::vector<int>& arr) {
    int n = arr.size();
    int logN = std::floor(std::log2(n)) + 1;
    std::vector<std::vector<int>> minST(n, std::vector<int>(logN));

    // Initialize the first column of the sparse table
    for (int i = 0; i < n; ++i) {
        minST[i][0] = i;
    }

    int j = 1;
    int pot = 1 << j; // 2^j
    while (pot <= n) {
        int i = 0;
        while (i + pot - 1 < n) {
            if (arr[minST[i][j - 1]] <= arr[minST[i + (1 << (j - 1))][j - 1]]) {
                minST[i][j] = minST[i][j - 1];
            } else {
                minST[i][j] = minST[i + (1 << (j - 1))][j - 1];
            }
            i++;
        }
        j++;
        pot = 1 << j; // Update 2^j
    }
    return minST;
}

// range minimum query
int rmq(const std::vector<int>& arr, const std::vector<std::vector<int>>& st, int l, int r) {
    int j = std::floor(std::log2(r - l + 1));
    if (arr[st[l][j]] <= arr[st[r - (1 << j) + 1][j]]) {
        return arr[st[l][j]];
    }
    return arr[st[r - (1 << j) + 1][j]];
}

int main() {
    int n, q;
    std::cin >> n >> q; // 1 <= n, q <= 2 * 10^5

    std::vector<int> arr(n);
    for (int i = 0; i < n; i++) {
        std::cin >> arr[i];
    }
    std::vector<std::vector<int>> queryCount(q + 1);
    bool areZeros = false;
    int maxTotal = 0;

    for (int i = 0; i < n; i++) {
        queryCount[arr[i]].push_back(i);
        maxTotal = std::max(maxTotal, arr[i]);
        if (arr[i] == 0) 
            areZeros = true;
    }

    if (maxTotal < q && maxTotal > 0 && areZeros) {
        arr[queryCount[0][0]] = q;
    }

    if (maxTotal == 0) {
        std::cout << "YES\n";
        for (int i = 0; i < n - 1; i++) {
            std::cout << q << " ";
        }
        std::cout << q << "\n";
        return 0;
    }

    if (!areZeros && maxTotal < q) {
        std::cout << "NO\n";
        return 0;
    }

    if (areZeros) {
        for (int i = 0; i < n; i++) {
            if (arr[i] == 0) {
                for (int j = i + 1; j < n; j++) {
                    if (arr[j] != 0) {
                        arr[i] = arr[j];
                        break;
                    }
                }
                if (arr[i] == 0) {
                    arr[i] = arr[i - 1];
                }
            }
        }
    }

    std::vector<std::vector<int>> minST = sparseTable(arr);

    for (int i = q; i > 0; i--) {
        if (queryCount[i].size() > 1) {
            int first = queryCount[i][0];
            int last = queryCount[i][queryCount[i].size() - 1];
            if (first == last) 
                continue;
            int minVal = rmq(arr, minST, first, last);
            if (minVal != i) {
                std::cout << "NO\n";
                return 0;
            }
        }
    }

    std::cout << "YES\n";
    for (int i = 0; i < n - 1; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << arr[n - 1] << "\n";

    return 0;
}