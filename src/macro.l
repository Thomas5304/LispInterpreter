;(testing (joke 2 3) (joke 3 4))
(define lst '(-1 2 3 8 9 20))

(defun chksqr (stple)
    (let ((len length(stple)))
        (defun chksqr-col (stple len)
            (if (!= (length(car(stpl))) len)
                nil
                (if (chksqr-col (cdr stpl) len)
                    t
                    nil
                )
            )
        )
        (chksqr-col stple len)
    )
)

(defun register-layer (&key stipple) (print-eval stipple)
)

(defmacro layer-definition (&rest clauses)

  `(register-layer
      ,@(apply append
            (mapcar (lambda (clause)

                (let ((key (car clause))
                    (value (cadr clause)))

                    (list (intern
                        (+ ":" key)
                        )
                        ,value
                    )
                )
            )

          clauses)
        )
    )
)

(defun plus2 (x) (+ x 2))
(defun multadd2 (&key m a) (* m (+ a 2)))
(print-eval (plus2 5))
(print-eval (multadd2 :m 4 :a 2))

(do-list (el lst) (print el))

(define chessboard '((0 1) (1 0)))



(print "Layer definition")

(print (chksqr chessboard))

(layer-definition (stipple chessboard))


(defun define-person (&key name vorname) (print (format "Vorname: {} Name: {}" vorname name)))

(defmacro person (&rest clauses)
    `(define-person ,@(apply append (mapcar
        (lambda (clause)

            (let ((key (car clause))
                (value (cadr clause)))

               (list (intern
                    (+ ":" key)
                    )
                    ,value
                )
            )
        )
        clauses
    )))
)

(person (name "Dilling") (vorname "Thomas"))

(apply append '('(test tom) '(case bla)))

;(define-person :name "Dilling" :vorname "Thomas")
;(exit)
