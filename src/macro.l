;(testing (joke 2 3) (joke 3 4))
(define lst '(-1 2 3 8 9 20))

(defun chksqr (stple)
    (let ((len (length stple)))
        (defun chksqr-col (list_of_list len)
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

(defun set-color (r g b)
  (list r g b)
  )

(defun register-layer (&key stipple (color (0 0 0)))
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
        (print "")
        (print "Layer:")
        (print "")
        (print (print-rows stipple))
        (print color)
        (print "")
        (print "")
    )
)


(defmacro layer-definition (&rest clauses)
  `(register-layer
    ,@(apply append (mapcar
                     (lambda (clause)

                       (let ((key (car clause))
                             (value (cadr clause)))
                         (cond
                          ((== key "color")
                             (define value (list (intern
                                    (+ "set-" key)
                                    )
                                   ,value ,(nth 2 clause) ,(nth 3 clause)
                                   )
                               )
                             )
                          )
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

(print-eval (null '(1 2)))
(print-eval (null '()))

(define chessboard '((0 0 1 1) (0 0 1 1) (1 1 0 0) (1 1 0 0)))
(define dash '((1 0 0 0)
               (0 1 0 0)
               (0 0 1 0)
               (0 0 0 1)))
(define error1 '((0 1) (1 0 1)))



(print "Layer definition")

(print-eval (chksqr error1))
(print-eval (chksqr dash))
(print-eval (chksqr chessboard))

(layer-definition (stipple chessboard) (color 30 20 50))
(layer-definition (stipple dash))

(print "\n\nPerson DSL test case\n")
(defun define-person (&key name vorname )
(print (format "Vorname: {} Name: {} Farbe: {}" vorname name 0)))

(defmacro person (&rest clauses)
  `(define-person
     ,@(apply append (mapcar
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
              clauses)
                      )

     )
  )

(person (name "Dilling") (vorname '("Thomas" "Heinrich")))
(defun-python handle-define-stipple (name display stipple) printStipple)

(defmacro drDefineStipple (&rest clauses)
  `(begin ,@(mapcar ,(lambda (clause)
                       (let ((DisplayName (nth 0 clause))
                             (StippleName (nth 1 clause))
                             (BitMap      (nth 2 clause)))
                         (print (format "DisplayName: {} StippleName: {}" DisplayName StippleName))
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
                         (print (print-rows BitMap))
                         (handle-define-stipple StippleName DisplayName BitMap)
                         0
                         )
                       )
                    clauses)
          )

  )
;(defmacro drDefineStipple (&rest clause)
;    `(begin (print "ignore drDefineStipple"))
;)

(drDefineStipple
;( DisplayName   StippleName  Bitmap     )
 ( display       dots         ( ( 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  ) ) )
 ( display       dots1        ( ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 1 0 0 0 1 0 0 0 1 0 0 0 1 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 1 0 0 0 1 0 0 0 1 0 0 0 1 0 0 0  ) ) )
 ( display       hLine        ( ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  )
                                ( 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1  ) ) )
 )
;(define-person :name "Dilling" :vorname "Thomas")
;(exit)
