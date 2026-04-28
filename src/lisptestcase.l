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
       
(defun sqr (x) (* x x))

(defmacro unless (cond body) (quasiquote (if (not (unquote cond)) (unquote body))))

(unless nil (define anhalter 42))
(unless t (define fehlt 42))

(print-env)
