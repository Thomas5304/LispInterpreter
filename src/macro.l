;(testing (joke 2 3) (joke 3 4))
(define lst '(-1 2 3 8 9 20))


(print-eval (plus2 5))
(print-eval (multadd2 :m 4 :a 2))

(defun test (a) (cond ((< a 0) (print "negativ"))
    ((< a 2) (print "small"))
    ((> a 9) (print "realy big"))
    (else (print "big"))
))

(map test lst)

(do-list (el lst) (print el))


(print "Layer definition")
(layer-definition (stipple '((1 0) (0 1))))
;(exit)
