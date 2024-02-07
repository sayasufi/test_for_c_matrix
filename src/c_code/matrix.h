#ifndef MATRIX_H_
#define MATRIX_H_

#include <math.h>

typedef double TWideVector[8];
typedef double TWideMatrix[8][8];
void  CopyWideMatr(short m, short n, TWideMatrix C_from, TWideMatrix C_to);
double AbsWideVect     (short n, TWideVector a);
void  AddWideVect     (short n, TWideVector a1, TWideVector a2, TWideVector a);
void  SubWideVect     (short n, TWideVector a1, TWideVector a2, TWideVector a);
void  MultWideVectScal(short n, TWideVector a1, double b, TWideVector a);
void  AddWideMatr     (short m, short n, TWideMatrix C1, TWideMatrix C2, TWideMatrix C);
void  SubWideMatr     (short m, short n, TWideMatrix C1, TWideMatrix C2, TWideMatrix C);
void  MultWideMatrMatr(short m1, short n1, short n2, TWideMatrix C1, TWideMatrix C2, TWideMatrix C);
void  MultWideMatrVect(short m, short n, TWideMatrix C1, TWideVector a1, TWideVector a);
void  MultWideMatrScal(short m, short n, TWideMatrix C1, double b, TWideMatrix C);
void  IdentityWide    (short m, TWideMatrix C);
void  TransposeWide   (short m, short n, TWideMatrix C, TWideMatrix CT);
void  SimilarityWide  (short m, short n, TWideMatrix B, TWideMatrix C, TWideMatrix C_);
void  InverseWide     (short n, TWideMatrix C, TWideMatrix C_1);
void  sort(int size, double arr[], double arr_out[]);

#endif
