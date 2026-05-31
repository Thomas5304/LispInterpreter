(print "start")

(defmacro macro-include (incfile)
  `(begin ,@(mapcar (lambda (x) x) (include ,(eval incfile))
          )
          )
  )

(defmacro macro-include-f (incfile)
    `(begin (print ,incfile)
          )
  )

(defun fun-include (incfile)
    (let ((function-mode nil))
        (include incfile)
    )
)

(defmacro test-variable (var) `(print "test" ,var))

;print (macroexpand (macro-include "included.l")))

;(print "flat include with string")
;(include "included.l")

;(print "macro include with string")
;(macro-include "included.l")

(let ((my-file "included.l"))
  ;(print "flat nclude with variable filename=" my-file)
  ;(print-eval (include my-file))
  ;(test-variable my-file)
  ;(print "macro include with variable filename=" my-file)
  ;(print (macroexpand (macro-include my-file)))
  (print "function include with variable filename=" my-file)
  (fun-include my-file)
  (print "finish")
  )
(exit)
