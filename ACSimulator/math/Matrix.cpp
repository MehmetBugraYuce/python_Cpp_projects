#include "Matrix.hpp"

Matrix::Matrix(size_t rows, size_t cols)
   : rows_(rows), cols_(cols), data_(rows * cols, std::complex<double>(0.0, 0.0)) {}

   std::complex<double>& Matrix::operator()(size_t r, size_t c) {
       if (r >= rows_ || c >= cols_) {
           throw std::out_of_range("Index out of range");
       }
       return data_[r * cols_ + c];
   }

   const std::complex<double>& Matrix::operator()(size_t r, size_t c) const {
       if (r >= rows_ || c >= cols_) {
           throw std::out_of_range("Index out of range");
       }
       return data_[r * cols_ + c];
   }

   void Matrix::swapRows(size_t r1, size_t r2) {
       if (r1 >= rows_ || r2 >= rows_) {
           throw std::out_of_range("Row index out of range");
       }
       for (size_t c = 0; c < cols_; ++c) {
           std::swap((*this)(r1, c), (*this)(r2, c));
       }
   }

    void Matrix::print() const {
         for (size_t i = 0; i < rows_; ++i) {
              for (size_t j = 0; j < cols_; ++j) 
                std::cout << (*this)(i, j) << "\t";
              std::cout << "\n";
         }
    }