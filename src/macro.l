;;(testing (joke 2 3) (joke 3 4))
;(define lst '(-1 2 3 8 9 20))
;
;(defun chksqr (stple)
;    (let ((len (length stple)))
;        (defun chksqr-col (list_of_list len)
;            (if (null list_of_list) t
;                (begin
;                    (define actlen (length (car list_of_list)))
;                    (and
;                        (== actlen len)
;                        (chksqr-col (cdr list_of_list) len)
;                    )
;                )
;            )
;        )
;        (chksqr-col stple len)
;    )
;)
;
;(defun set-color (r g b)
;  (list r g b)
;  )
;
;(defun register-layer (&key stipple (color (0 0 0)))
;    (let ((len (length stipple)))
;        (defun print-row (row)
;            (if (null row)
;                ""
;                (+ (if (== (car row) 0)
;                        " "
;                        "X"
;                    )
;                    (print-row (cdr row))
;                )
;            )
;        )
;        (defun print-rows (rows)
;            (if (null rows)
;                ""
;                (+  (print-row (car rows)) "\n"
;                    (print-rows (cdr rows))
;                )
;            )
;            )
;        (print "")
;        (print "Layer:")
;        (print "")
;        (print (print-rows stipple))
;        (print color)
;        (print "")
;        (print "")
;    )
;)
;
;
;(defmacro layer-definition (&rest clauses)
;  `(register-layer
;    ,@(apply append (mapcar
;                     (lambda (clause)
;
;                       (let ((key (car clause))
;                             (value (cadr clause)))
;                         (cond
;                          ((== key "color")
;                             (define value (list (intern
;                                    (+ "set-" key)
;                                    )
;                                   ,value ,(nth 2 clause) ,(nth 3 clause)
;                                   )
;                               )
;                             )
;                          )
;                         (list (intern
;                                (+ ":" key)
;                                )
;                               ,value
;                               )
;                           )
;                         )
;
;             clauses)
;                       )
;                     )
;    )
;
;(defun plus2 (x) (+ x 2))
;(defun multadd2 (&key m a) (* m (+ a 2)))
;(print-eval (plus2 5))
;(print-eval (multadd2 :m 4 :a 2))
;
;(do-list (el lst) (print el))
;
;(print-eval (null '(1 2)))
;(print-eval (null '()))
;
;(define chessboard '((0 0 1 1) (0 0 1 1) (1 1 0 0) (1 1 0 0)))
;(define dash '((1 0 0 0)
;               (0 1 0 0)
;               (0 0 1 0)
;               (0 0 0 1)))
;(define error1 '((0 1) (1 0 1)))
;
;
;
;(print "Layer definition")
;
;(print-eval (chksqr error1))
;(print-eval (chksqr dash))
;(print-eval (chksqr chessboard))
;
;(layer-definition (stipple chessboard) (color 30 20 50))
;(layer-definition (stipple dash))
;
;(print "\n\nPerson DSL test case\n")
;(defun define-person (&key name vorname )
;(print (format "Vorname: {} Name: {} Farbe: {}" vorname name 0)))
;
;(defmacro person (&rest clauses)
;  `(define-person
;     ,@(apply append (mapcar
;                      (lambda (clause)
;
;                        (let ((key (car clause))
;                              (value (cadr clause)))
;
;                          (list (intern
;                                 (+ ":" key)
;                                 )
;                                ,value
;                                )
;                          )
;                        )
;              clauses)
;                      )
;
;     )
;  )
;
;(person (name "Dilling") (vorname '("Thomas" "Heinrich")))
(defun-python handle-define-stipple (name display stipple) createStipple displayDRF)
(defun-python handle-define-lpp (layer purpose (&optional stippleName)) createLPP displayDRF)
(defun-python handle-define-layer (layer) createLayer displayDRF)
(defun-python handle-define-purpose (purpose) createPurpose displayDRF)


(defmacro drDefineStipple (&rest clauses)
  `(begin ,@(mapcar ,(lambda (clause)
                       (let ((DisplayName (nth 0 clause))
                             (StippleName (nth 1 clause))
                             (BitMap      (nth 2 clause)))
                         (handle-define-stipple StippleName DisplayName BitMap)
                         0
                         )
                       )
                    clauses)
          )
  )

(defmacro dfLayerTable (&rest clauses)
  `(begin ,@(mapcar ,(lambda (clause)
                       (let ((layerName   (nth 0 clause))
                             (purposeName (nth 1 clause))
                             (stippleName (if (>= (length clause) 3)
                                          (nth 2 clause)
                                          ""))
                            )
                            (handle-define-lpp layerName purposeName stippleName)
                            0
                        )
                      )
             clauses
            )
    )
  )

(defmacro dfLayer (&rest clauses)
  `(begin ,@(mapcar ,(lambda (clause)
                       (let ((layerName   (nth 0 clause)))
                            (handle-define-layer layerName)
                            0
                        )
                      )
             clauses
            )
    )
  )

(defmacro dfPurpose (&rest clauses)
  `(list ,@(mapcar ,(lambda (clause)
                       (let ((purposeName   (nth 0 clause)))
                            (handle-define-purpose purposeName)
                            0
                        )
                      )
             clauses
            )
    )
  )

(print "load display.drf")
(let ((function-mode t))
 (eval (include "small.display.drf"))
  )
;(define-person :name "Dilling" :vorname "Thomas")
(print "testcase" '(my-and (== 1 1) (> 2 1) (< 1 2)))
(print-eval (my-and (== 1 1) (> 2 2) (< 1 2)))
(print "testcase expanded: " (macroexpand-1 (my-and (== 1 1) (> 2 1) (< 3 3))))

(defmacro test (&rest a)
    `(+ 10 ,@a))

(print (macroexpand (test 2 3)))
(print (test 2 3))

(print (cond ((== 1 2) "test1")
             ((== 2 3) "test2")
             (t        "test3")
        )
)
(print (null '()))
(print (null '(1 2)))
(print (null (cdr '( 2))))
(print (macroexpand-1 (dfPurpose (ma1) (ma2))))
(print (macroexpand (my-cond ((== 1 2) "test1")
             ((== 3 3) "test2")
             (t        "test3")
        )
        )
)
(print (my-cond ((== 1 2) "test1")
             ((== 3 3) "test2")
             (t        "test3")
        )
)

(print (macroexpand-1 
    (when (> 1 0) (+ 1 2) (* 2 2 2) )
))
(print
    (when (> 1 0) (+ 1 2) (* 2 2 2) )
)
(print (macroexpand-1
    (unless (> 1 0) (+ 1 2) (* 2 2 2) )
))
(print
    (unless (> 1 0) (+ 1 2) (* 2 2 2) )
)
(for i from 2 to 11
    (print i " = " (* i i))
    (print )
    )
(exit)
