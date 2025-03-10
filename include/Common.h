#pragma once

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>

typedef int BOOL;

typedef signed char s8;
typedef signed short s16;
typedef signed long s32;
typedef signed long long s64;

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned long u32;
typedef unsigned long long u64;

typedef float f32;
typedef double f64;

#define MIN(a, b)               \
    ({                          \
        __typeof__(a) _a = (a); \
        __typeof__(b) _b = (b); \
        _a < _b ? _a : _b;      \
    })
#define MAX(a, b)               \
    ({                          \
        __typeof__(a) _a = (a); \
        __typeof__(b) _b = (b); \
        _a > _b ? _a : _b;      \
    })

#define UNUSED(x) UNUSED_##x __attribute__((__unused__))

#define CONTAINER_OF(ptr, type, member) \
    ((type *)((char *)(1 ? (ptr) : &((type *)0)->member) - offsetof(type, member)))

#define BUILD_BUG_ON_ZERO(e) ((int)(sizeof(struct { int : (-!!(e)); })))
#define SAME_TYPE(a, b) __builtin_types_compatible_p(typeof(a), typeof(b))
#define MUST_BE_ARRAY(a) BUILD_BUG_ON_ZERO(SAME_TYPE((a), &(a)[0]))
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]) + MUST_BE_ARRAY(arr))

enum {
    REGION_P = 0x54a9,
    REGION_E = 0x5409,
    REGION_J = 0x53cd,
    REGION_K = 0x5511,
};

#define REGION (*(u16 *)0x8000620a)

#if !defined(NO_NEW_DELETE) && \
        !defined(__cplusplus)  // new/delete are reserved identifiers in C++
void *new (size_t size);

void delete (void *memBlock);
#endif

typedef struct {
    f32 x;
    f32 y;
} Vec2;

typedef struct {
    f32 x;
    f32 y;
    f32 z;
} Vec3;

enum {
    PATCH_TYPE_WRITE = 0x0,
    PATCH_TYPE_BRANCH = 0x1,
};

typedef struct {
    u32 type;
    union {
        struct {
            void *dst;
            void *src;
            u32 size;
        } write;
        struct {
            void *from;
            void *to;
            bool link;
        } branch;
    };
} Patch;

#define PATCH_S16(function, offset, value) \
    __attribute__((section("patches"))) \
    extern const Patch patch_ ## function ## offset = { \
        .type = PATCH_TYPE_WRITE, \
        .write = { \
            (&function + offset), \
            &(s16) { (value) }, \
            sizeof(s16), \
        }, \
    }

#define PATCH_U32(function, offset, value) \
    __attribute__((section("patches"))) \
    extern const Patch patch_ ## function ## offset = { \
        .type = PATCH_TYPE_WRITE, \
        .write = { \
            (&function + offset), \
            &(u32) { (value) }, \
            sizeof(u32), \
        }, \
    }

#define PATCH_NOP(function, offset) PATCH_U32(function, offset, 0x60000000)

#define PATCH_BRANCH(from, to, link) \
    __attribute__((section("patches"))) \
    extern const Patch patch_ ## to = { \
        .type = PATCH_TYPE_BRANCH, \
        .branch = { \
            &from, \
            &to, \
            link, \
        }, \
    }

#define PATCH_B(from, to) \
    PATCH_BRANCH(from, to, false)

#define PATCH_BL(from, to) \
    PATCH_BRANCH(from, to, true)
