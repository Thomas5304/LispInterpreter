;(testing (joke 2 3) (joke 3 4))
(define lst '(-1 2 3 8 9 20))

(defun chksqr (stple)
    (let ((len (length stple)))
        (defun chksqr-col (list_of_list len)
;            (cond
;                ((null list_of_list)  t)
;                ((!= (length (car list_of_list)) len) nil)
;                (else (chksqr-col (cdr list_of_list) len))
;            )
            (if (null list_of_list) t
                (begin
                    (define actlen (length (car list_of_list)))
                    (and
                        (== actlen len)
                        (chksqr-col (cdr list_of_list) len)
                    )
                )
            )
        )
        (chksqr-col stple len)
    )
)

(defun register-layer (&key stipple color) 
    (let ((len (length stipple)))
        (defun print-row (row)
            (if (null row)
                ""
                (+ (if (== (car row) 0)
                        " "
                        "X"
                    )
                    (print-row (cdr row))
                )
            )
        )
        (defun print-rows (rows)
            (if (null rows)
                ""
                (+  (print-row (car rows)) "\n"
                    (print-rows (cdr rows))
                )
            )
        )
        (print (print-eval stipple))
        (print color)
    )
)
            

(defmacro layer-definition (&rest clauses)

  `(register-layer
      ,@(apply append
            (mapcar (lambda (clause)

                (let ((key (car clause))
                    (value (cadr clause)))
                    (if (== key "color")
                        (list (intern (format "set-{}" key)) ,value)
                        (list (intern
                            (+ ":" key)
                            )
                            ,value
                        )
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

(print-eval (null '(1 2)))
(print-eval (null '()))

(define chessboard '((0 0 1 1) (1 1 0 0)))
(define dash '((1 0 0 0)
               (0 1 0 0)
               (0 0 1 0)
               (0 0 0 1)))
(define error1 '((0 1) (1 0 1)))



(print "Layer definition")

(print-eval (chksqr chessboard))
(print-eval (chksqr error1))

(layer-definition (stipple chessboard dash) (color 5 20 40))

(print "\n\nPerson DSL test case\n")
(defun define-person (&key name vorname)
(print (format "Vorname: {} Name: {} Farbe: {}" vorname name farbe)))

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

(person (name "Dilling") (vorname '("Thomas" "Heinrich")))

(apply append '('(test tom) '(case bla)))

;(define-person :name "Dilling" :vorname "Thomas")
;(exit)
