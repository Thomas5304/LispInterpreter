(print "start")

(defmacro macro-include (filename)
  `(begin ,@(include filename)
          )
  )

(print (macroexpand-1 (macro-include "included.l")))

(let ((filename "included.l"))
  (print "including" filename)
  (macro-include filename)
  (print "finish")
  )
(exit)
