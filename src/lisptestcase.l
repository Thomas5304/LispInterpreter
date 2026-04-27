(let (
    (x 10)
    (y 20)
    (z (+ x y))
    )

        (print x y z)

)

(defun fib (x)
   (if (> 3 x) (+ (fib (- x 1)) (fib (- x 2))) (1))
