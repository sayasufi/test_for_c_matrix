//#include "Matrix.h"

#include "matrix.h"
#include <stddef.h>
//#include "../term_messaging.h"

void CopyWideMatr(short m, short n, TWideMatrix C_from, TWideMatrix C_to) {
	//copies C_from to C_to

	short i, j;
	for (i = 0; i < m; i++)
		for (j = 0; j < n; j++)
			C_to[i][j] = C_from[i][j];
}

double AbsWideVect(short n, TWideVector a) {
	double r = 0;
	short i = 0;

	for (i = 0; i < n; i++)
		r += a[i] * a[i];
	return sqrt(r);
}

void AddWideVect(short n, TWideVector a1, TWideVector a2, TWideVector a) {
	//a = a1 + a2
	short i;

	for (i = 0; i < n; i++)
		a[i] = a1[i] + a2[i];
}

void SubWideVect(short n, TWideVector a1, TWideVector a2, TWideVector a) {
	//a = a1 - a2
	short i;

	for (i = 0; i < n; i++)
		a[i] = a1[i] - a2[i];
}

void MultWideVectScal(short n, TWideVector a1, double b, TWideVector a) {
	//a = a1 * b
	short i;

	for (i = 0; i < n; i++)
		a[i] = a1[i] * b;
}

void AddWideMatr(short m, short n, TWideMatrix C1, TWideMatrix C2,
		TWideMatrix C) {
	//C = C1 + C2
	short i, j;

	for (i = 0; i < m; i++)
		for (j = 0; j < n; j++)
			C[i][j] = C1[i][j] + C2[i][j];
}

void SubWideMatr(short m, short n, TWideMatrix C1, TWideMatrix C2,
		TWideMatrix C) {
	//C = C1 - C2
	short i, j;

	for (i = 0; i < m; i++)
		for (j = 0; j < n; j++)
			C[i][j] = C1[i][j] - C2[i][j];
}

void MultWideMatrMatr(short m1, short n1, short n2, TWideMatrix C1,
		TWideMatrix C2, TWideMatrix C) {
	//C = C1 * C2
	short i, j, k;

	for (i = 0; i < m1; i++)
		for (j = 0; j < n2; j++)
			for (C[i][j] = 0, k = 0; k < n1; k++)
				C[i][j] += C1[i][k] * C2[k][j];
}

void MultWideMatrVect(short m, short n, TWideMatrix C1, TWideVector a1,
		TWideVector a) {
	// a = C1 * a1
	short i, j;

	for (i = 0; i < m; i++) {
		a[i] = 0;
		for (j = 0; j < n; j++)
			a[i] += C1[i][j] * a1[j];
	}
}

void MultWideMatrScal(short m, short n, TWideMatrix C1, double b, TWideMatrix C) {
	//C = C1 * b
	short i, j;

	for (i = 0; i < m; i++)
		for (j = 0; j < n; j++)
			C[i][j] = C1[i][j] * b;
}
void AddWideMatrScal(short m, short n, TWideMatrix C1, double b, TWideMatrix C) {
	//C = C1 + b
	short i, j;

	for (i = 0; i < m; i++)
		for (j = 0; j < n; j++)
			C[i][j] = C1[i][j] + b;
}

void IdentityWide(short m, TWideMatrix C) {
	short i, j;
	for (i = 0; i < m; i++)
		for (j = 0; j < m; j++)
			C[i][j] = (i == j) ? 1.0 : 0.0;
}

void TransposeWide(short m, short n, TWideMatrix C, TWideMatrix CT) {
	short i, j;

	for (i = 0; i < m; i++)
		for (j = 0; j < n; j++)
			CT[j][i] = C[i][j];
}

void SimilarityWide(short m, short n, TWideMatrix B, TWideMatrix C,
		TWideMatrix C_) {
//  C_ = B  * C  * BT
//  mm   mn   nn   nm

	TWideMatrix BT, BC;

	MultWideMatrMatr(m, n, n, B, C, BC);
	TransposeWide(m, n, B, BT);
	MultWideMatrMatr(m, n, m, BC, BT, C_);
}

void InverseWide(short n, TWideMatrix C, TWideMatrix C_1) {
//C * C_1 = I

	double big, fabval, pivinv, temp;
	short i, j, k, l, ll;
	short icol = 0;
	short irow = 0;
	short indxc[9] = {0};
	short indxr[9] = {0};
	short ipiv[9] = {0};

	for (i = 0; i < n; i++)
		for (j = 0; j < n; j++)
			C_1[i][j] = C[i][j];

	for (j = 0; j < n; j++)
		ipiv[j] = 0;

	for (i = 0; i < n; i++) {
		big = 0.0;
		for (j = 0; j < n; j++)
			if (ipiv[j] != 1)
				for (k = 0; k < n; k++) {
					if (ipiv[k] == 0) {
						if (C_1[j][k] < 0)
							fabval = -C_1[j][k];
						else
							fabval = C_1[j][k];

						if (fabval >= big) {
							big = fabval;
							irow = j;
							icol = k;
						}
					} else {
						//singular matrix
					}
				}
//		if (icol > 9){
//			term_ERRmsg("[TOOL] Detected out of range in matrix.c");
//		}


		(ipiv[icol])++;

		if (irow != icol)
			for (l = 0; l < n; l++) {
				temp = C_1[irow][l];
				C_1[irow][l] = C_1[icol][l];
				C_1[icol][l] = temp;
			}

		indxr[i] = irow;
		indxc[i] = icol;

		pivinv = 1.0 / C_1[icol][icol];
		C_1[icol][icol] = 1.0;
		for (l = 0; l < n; l++)
			C_1[icol][l] *= pivinv;

		for (ll = 0; ll < n; ll++)
			if (ll != icol) {
				temp = C_1[ll][icol];
				C_1[ll][icol] = 0.0;
				for (l = 0; l < n; l++)
					C_1[ll][l] -= C_1[icol][l] * temp;
			}
	}

	for (l = n - 1; l >= 0; l--) {
		if (indxr[l] != indxc[l])
			for (k = 0; k < n; k++) {
				temp = C_1[k][indxr[l]];
				C_1[k][indxr[l]] = C_1[k][indxc[l]];
				C_1[k][indxc[l]] = temp;
			}
	}

}

void sort(int size, double arr[], double arr_out[]) {
	// ���������� ����������� ������� �� �����������
	int pass; //������� ��������
	size_t i;
	double hold; //��������� ��������� ��� ������ ���������
	for (i = 0; i < size; ++i) {
		arr_out[i] = arr[i];
	}
	for (pass = 1; pass < size; ++pass) {
		for (i = 0; i < (size - 1); ++i) {
			if (arr_out[i] > arr_out[i + 1]) {
				hold = arr_out[i];
				arr_out[i] = arr_out[i + 1];
				arr_out[i + 1] = hold;
			}
		}
	}
}
