//This is the main file for the project.

#include "math/LinearSolver.hpp"
#include <iostream>

int main() {

    Matrix A(2,2);

    A(0,0) = {2,0};
    A(0,1) = {1,0};
    A(1,0) = {5,0};
    A(1,1) = {7,0};

    std::vector<std::complex<double>> b = {
        {11,0},
        {13,0}
    };

    auto x = LinearSolver::solveGaussian(A, b);

    for (auto& val : x)
        std::cout << val << "\n";
}