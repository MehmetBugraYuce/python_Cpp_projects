#pragma once
#include <vector>
#include <complex>
#include <stdexcept>
#include <iostream>

class Matrix {
    private:
        size_t rows_;
        size_t cols_;
        std::vector<std::complex<double>> data_;

    public:
        Matrix(size_t rows, size_t cols);

        size_t rows() const {return rows_;}
        size_t cols() const {return cols_;}

        std::complex<double>& operator()(size_t r, size_t c);
        const std::complex<double>& operator()(size_t r, size_t c) const;

        void swapRows(size_t r1, size_t r2);

        void print() const;

};