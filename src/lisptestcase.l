(let (
    (x 10)
    (y 20)
    (z (+ x y))
    )


(defun fib (x) (if (> 3 x) (+ (fib (- x 1)) (fib (- x 2))) (1))

(print (map fib ( 3 4 5 6)))
(print-env)
(fib 6)
       

)
