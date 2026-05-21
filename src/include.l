(print "start")

(defmacro macro-include (filename)
  `( ,@(mapcar (lambda (x) x) (include filename)
          )
          )
  )

(print (macroexpand (macro-include "included.l")))

(let ((filename "included.l"))
  (print "including" filename)
  (macro-include filename)
  (print "finish")
  )
(exit)
