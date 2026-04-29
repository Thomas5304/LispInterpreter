(defmacro unless (cond body) (quasiquote (if (not (unquote cond)) (unquote body))))
(unless t (print "Fail"))

(unless nil (print "Pass"))
(debug 0)
(defun range (max)
(let ((i 0) (res (list)))
  (while (< i max)
    (cons res i)
    (define i (+ i 1))
    )
  res
  ))
(defun pwr (x y) (if (> y 0) (* x (pwr x (- y 1))) 1))
(print (map (lambda (x) (pwr 2 x)) (range 10)))
(debug 0)
(define mylist '(1 2 3 4))
(cdr (cdr(cdr mylist)))

(defun azip (l1 l2) (let ((l1e (car l1))
                         (l2e (car l2))
                         )
                     (if (and l1e l2e) 
                       (result (list l1e l2e))
                       (list )
                       )))

                     
(define mylist (range 5))
(print mylist)
(define zipped (zip mylist (map (lambda (x) (pwr 2 x)) mylist)))
(print zipped)

(print (zip '(1 2 3 4) '(1 3 5 7) '(2 4 6 8)))
