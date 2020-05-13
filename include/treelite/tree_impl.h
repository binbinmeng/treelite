/*!
 * Copyright 2020 by Contributors
 * \file tree_impl.h
 * \brief Implementation for tree.h
 * \author Hyunsu Cho
 */
#ifndef TREELITE_TREE_IMPL_H_
#define TREELITE_TREE_IMPL_H_

namespace treelite {

template <typename T>
ContiguousArray<T>::ContiguousArray()
  : buffer_(nullptr), size_(0), capacity_(0), owned_buffer_(true) {}

template <typename T>
ContiguousArray<T>::~ContiguousArray() {
  if (buffer_ && owned_buffer_) {
    std::free(buffer_);
  }
}

template <typename T>
ContiguousArray<T>::ContiguousArray(ContiguousArray&& other)
  : buffer_(other.buffer_), size_(other.size_), capacity_(other.capacity_),
    owned_buffer_(other.owned_buffer_) {
  other.buffer_ = nullptr;
  other.size_ = other.capacity_ = 0;
}

template <typename T>
ContiguousArray<T>&
ContiguousArray<T>::operator=(ContiguousArray&& other) {
  if (buffer_ && owned_buffer_) {
    std::free(buffer_);
  }
  buffer_ = other.buffer_;
  size_ = other.size_;
  capacity_ = other.capacity_;
  owned_buffer_ = other.owned_buffer_;
  other.buffer_ = nullptr;
  other.size_ = other.capacity_ = 0;
  return *this;
}

template <typename T>
inline ContiguousArray<T>
ContiguousArray<T>::Clone() const {
  ContiguousArray clone;
  clone.buffer_ = static_cast<T*>(std::malloc(sizeof(T) * capacity_));
  CHECK(clone.buffer_);
  std::memcpy(clone.buffer_, buffer_, sizeof(T) * size_);
  clone.size_ = size_;
  clone.capacity_ = capacity_;
  clone.owned_buffer_ = true;
  return clone;
}

template <typename T>
inline void
ContiguousArray<T>::UseForeignBuffer(void* prealloc_buf, size_t size) {
  if (buffer_ && owned_buffer_) {
    std::free(buffer_);
  }
  buffer_ = static_cast<T*>(prealloc_buf);
  size_ = size;
  capacity_ = size;
  owned_buffer_ = false;
}

template <typename T>
inline T*
ContiguousArray<T>::Data() {
  return buffer_;
}

template <typename T>
inline const T*
ContiguousArray<T>::Data() const {
  return buffer_;
}

template <typename T>
inline T*
ContiguousArray<T>::End() { 
  return &buffer_[Size()];
}

template <typename T>
inline const T*
ContiguousArray<T>::End() const {
  return &buffer_[Size()];
}

template <typename T>
inline T&
ContiguousArray<T>::Back() {
  return buffer_[Size() - 1];
}

template <typename T>
inline const T&
ContiguousArray<T>::Back() const {
  return buffer_[Size() - 1];
}

template <typename T>
inline size_t
ContiguousArray<T>::Size() const {
  return size_;
}

template <typename T>
inline void
ContiguousArray<T>::Reserve(size_t newsize) {
  CHECK(owned_buffer_) << "Cannot resize when using a foreign buffer; clone first";
  T* newbuf = static_cast<T*>(std::realloc(static_cast<void*>(buffer_), sizeof(T) * newsize));
  CHECK(newbuf);
  buffer_ = newbuf;
  capacity_ = newsize;
}

template <typename T>
inline void
ContiguousArray<T>::Resize(size_t newsize) {
  CHECK(owned_buffer_) << "Cannot resize when using a foreign buffer; clone first";
  if (newsize > capacity_) {
    size_t newcapacity = capacity_;
    if (newcapacity == 0) {
      newcapacity = 1;
    }
    while (newcapacity <= newsize) {
      newcapacity *= 2;
    }
    Reserve(newcapacity);
  }
  size_ = newsize;
}

template <typename T>
inline void
ContiguousArray<T>::Resize(size_t newsize, T t) {
  CHECK(owned_buffer_) << "Cannot resize when using a foreign buffer; clone first";
  size_t oldsize = Size();
  Resize(newsize);
  for (size_t i = oldsize; i < newsize; ++i) {
    buffer_[i] = t;
  }
}

template <typename T>
inline void
ContiguousArray<T>::Clear() {
  CHECK(owned_buffer_) << "Cannot clear when using a foreign buffer; clone first";
  Resize(0);
}

template <typename T>
inline void
ContiguousArray<T>::PushBack(T t) {
  CHECK(owned_buffer_) << "Cannot add element when using a foreign buffer; clone first";
  if (size_ == capacity_) {
    Reserve(capacity_ * 2);
  }
  buffer_[size_++] = t;
}

template <typename T>
inline void
ContiguousArray<T>::Extend(const std::vector<T>& other) {
  CHECK(owned_buffer_) << "Cannot add elements when using a foreign buffer; clone first";
  size_t newsize = size_ + other.size();
  if (newsize > capacity_) {
    size_t newcapacity = capacity_;
    if (newcapacity == 0) {
      newcapacity = 1;
    }
    while (newcapacity <= newsize) {
      newcapacity *= 2;
    }
    Reserve(newcapacity);
  }
  std::memcpy(&buffer_[size_], static_cast<const void*>(other.data()), sizeof(T) * other.size());
  size_ = newsize;
}

template <typename T>
inline T&
ContiguousArray<T>::operator[](size_t idx) {
  return buffer_[idx];
} 

template <typename T>
inline const T&
ContiguousArray<T>::operator[](size_t idx) const {
  return buffer_[idx];
} 

}  // namespace treelite
#endif  // TREELITE_TREE_IMPL_H_
