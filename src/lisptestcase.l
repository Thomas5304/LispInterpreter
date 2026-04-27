(let (
    (x 10)
    (y 20)
    (z (+ x y))
    )
  (print z)


)
(defun fib (x) (if (>= x 3) (+ (fib (- x 1)) (fib (- x 2))) 1))

(print (map fib ( 3 4 5 6 7 8 9 10)))
(fib 6)
       
