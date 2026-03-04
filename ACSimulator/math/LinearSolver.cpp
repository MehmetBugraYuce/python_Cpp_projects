#include "LinearSolver.hpp"
#include <cmath>

std::vector<std::complex<double>> LinearSolver::solveGaussian(Matrix A,std::vector<std::complex<double>> b)

{
    size_t n = A.rows();

    if(A.rows() != A.cols() || A.rows() != b.size()) {
        throw std::invalid_argument("Matrix A must be square and compatible with vector b");
    }

    // Forward elimination
    for (size_t k = 0; k < n; ++k) {

        // === Partial Pivoting ===
        size_t pivotRow = k;
        double maxVal = std::abs(A(k, k));

        for (size_t i = k + 1; i < n; ++i) {
            if (std::abs(A(i, k)) > maxVal) {
                maxVal = std::abs(A(i, k));
                pivotRow = i;
            }
        }

        if (std::abs(A(pivotRow, k)) < 1e-12)
            throw std::runtime_error("Matrix is singular");

        if (pivotRow != k) {
            A.swapRows(k, pivotRow);
            std::swap(b[k], b[pivotRow]);
        }
        // Eliminate the column
        for (size_t i = k + 1; i < n; ++i) {
            std::complex<double> factor = A(i, k) / A(k, k);
            for (size_t j = k; j < n; ++j) {
                A(i, j) -= factor * A(k, j);
            }
            b[i] -= factor * b[k];
        }
    }

    // Back substitution
    std::vector<std::complex<double>> x(n);
    for (int i = static_cast<int>(n) - 1; i >= 0; --i) {
        std::complex<double> sum = b[i];

        for (size_t j = i + 1; j < n; ++j)
            sum -= A(i, j) * x[j];

        x[i] = sum / A(i, i);
    }
    return x;
}