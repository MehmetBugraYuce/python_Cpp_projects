#pragma once
#include "Matrix.hpp"
#include <vector>

class LinearSolver {
    public:
        static std::vector<std::complex<double>> solveGaussian(Matrix A,std::vector<std::complex<double>> b);
};