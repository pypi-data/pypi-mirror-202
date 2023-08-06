

from numpy import zeros,array
import matplotlib.pyplot as plt

def jacobi(A,b,n):
  x1 =zeros(n)
  x2 =zeros(n)
  x3 =zeros(n)

  x1[0] = 0.0
  x2[0] = 0.0
  x3[0] = 0.0 
  print('%7s %9s %9s %9s'%('k','x1','x2','x3'))
  print("%7d %9.5f %9.5f %9.5f" % (0, x1[0], x2[0], x3[0]))

  for k in range(n - 1):
      x1[k + 1] = (b[0] + A[0,1] * x2[k] - A[0,2] * x3[k]) / A[0,0]
      x2[k + 1] = (b[1] + A[1,0] * x1[k] - A[1,2] * x3[k]) / A[1,1]
      x3[k + 1] = (b[2] + A[2,0] * x1[k] - A[2,1] * x2[k]) / A[2,2]
      print("%7d %9.5f %9.5f %9.5f" % (k + 1, x1[k + 1], x2[k + 1], x3[k + 1]))
  return x1,x2,x3

def jacobi_plt_print(A,b,n):
  x1 =zeros(n)
  x2 =zeros(n)
  x3 =zeros(n)

  x1[0] = 0.0
  x2[0] = 0.0
  x3[0] = 0.0

  for k in range(n - 1):
      x1[k + 1] = (b[0] + A[0,1] * x2[k] - A[0,2] * x3[k]) / A[0,0]
      x2[k + 1] = (b[1] + A[1,0] * x1[k] - A[1,2] * x3[k]) / A[1,1]
      x3[k + 1] = (b[2] + A[2,0] * x1[k] - A[2,1] * x2[k]) / A[2,2]

  x = range(n)
  y = x1
  y1 = x2
  y2 = x3
  plt.plot(x, y, 'b--', label='x1')
  plt.plot(x, y1, 'r', label='x2')
  plt.plot(x, y2, 'g', label='x3')
  plt.legend()
  plt.title('jacobi')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.show()

