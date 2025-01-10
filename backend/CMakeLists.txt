# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(hasami_shogi)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Додаємо опцію для створення DLL
if(WIN32)
    add_definitions(-DBUILDING_DLL)
endif()

# Створюємо shared library
add_library(hasami_shogi SHARED
    src/board.cpp
    src/game.cpp
    src/piece.cpp
    src/exports.cpp
)

# Включаємо директорію з хедерами
target_include_directories(hasami_shogi PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

# Встановлюємо вихідну директорію для бібліотеки
set_target_properties(hasami_shogi PROPERTIES 
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/lib"
    PREFIX ""
)