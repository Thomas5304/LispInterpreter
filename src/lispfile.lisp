(defun cadr (lst) (car (cdr lst)))

(defmacro layer-definition (&rest clauses)

  `(register-layer
      ,@(apply #'append
          (mapcar
            (lambda (clause)

              (let ((key (car clause))
                    (value (cadr clause)))

                (list
                  (intern
                    (concatenate 'string ":" (symbol-name key)))
                  `',value)))

            clauses))))


(defun register-layer (&rest specs) (print-eval specs))

;(defmacro layer-definition (&rest clauses)
;
;  `(register-layer
;     ,clauses))



(defun plus2 (x) (+ 2 x))
(defun multadd2 (&keys m a) (* m (+ a 2)))
