(print "start")

(defmacro macro-include (incfile)
  `(begin ,@(mapcar (lambda (x) x) ,(include incfile)
          )
          )
  )

(defmacro macro-include-f (incfile)
    `(begin (print ,incfile)
          )
  )

(print (macroexpand (macro-include "included.l")))

;(print "flat include with string")
;(include "included.l")

;(print "macro include with string")
;(macro-include "included.l")

(let ((my-file "included.l"))
  ;(print "flat nclude with variable filename=" my-file)
  ;(print-eval (include my-file))
  (print "macro include with variable filename=" my-file)
  (print (macroexpand (macro-include my-file)))
  ;(print "finish")
  )x
(exit)
