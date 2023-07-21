'use strict';

var cibKubernetes = ["32 32", "<path d='M13.604 19.136l0.011 0.009-1.333 3.219c-1.276-0.817-2.251-2.036-2.765-3.463l3.437-0.584 0.005 0.005c0.457-0.083 0.828 0.38 0.645 0.813zM12.495 16.297c0.453-0.125 0.584-0.704 0.229-1.011l0.005-0.016-2.615-2.339c-0.797 1.297-1.141 2.828-0.975 4.339l3.349-0.964zM14.021 13.656c0.38 0.276 0.911 0.016 0.932-0.453l0.016-0.005 0.197-3.495c-1.516 0.177-2.927 0.855-4.016 1.928l2.865 2.025zM15.036 17.323l0.964 0.464 0.964-0.464 0.239-1.036-0.667-0.833h-1.072l-0.667 0.833zM17.036 13.193c0.016 0.468 0.552 0.728 0.933 0.447l0.009 0.005 2.844-2.015c-1.083-1.063-2.484-1.74-3.989-1.923l0.197 3.485zM31.536 21.156l-7.697 9.573c-0.407 0.5-1.016 0.792-1.661 0.792l-12.349 0.005c-0.645 0-1.26-0.292-1.667-0.797l-7.697-9.573c-0.401-0.5-0.552-1.156-0.412-1.787l2.751-11.937c0.14-0.629 0.561-1.151 1.151-1.432l11.12-5.317c0.583-0.276 1.265-0.276 1.848 0l11.125 5.312c0.584 0.281 1.005 0.808 1.151 1.432l2.751 11.943c0.14 0.625-0.011 1.281-0.412 1.787zM27.151 18.412c-0.057-0.011-0.135-0.037-0.192-0.048-0.235-0.041-0.423-0.031-0.641-0.047-0.463-0.052-0.848-0.088-1.192-0.197-0.141-0.052-0.24-0.219-0.287-0.292l-0.271-0.079c0.145-1.036 0.099-2.088-0.141-3.109-0.233-1.025-0.656-2.004-1.244-2.88 0.068-0.063 0.197-0.176 0.233-0.213 0.011-0.12 0-0.244 0.125-0.375 0.265-0.251 0.595-0.453 0.989-0.699 0.193-0.109 0.365-0.181 0.557-0.323 0.043-0.031 0.1-0.083 0.147-0.12 0.317-0.249 0.391-0.692 0.161-0.979s-0.672-0.312-0.989-0.063c-0.047 0.037-0.109 0.084-0.152 0.12-0.176 0.156-0.285 0.307-0.437 0.469-0.328 0.333-0.604 0.609-0.9 0.807-0.125 0.079-0.319 0.052-0.401 0.047l-0.256 0.183c-1.457-1.532-3.421-2.484-5.525-2.672l-0.016-0.297c-0.088-0.083-0.192-0.156-0.219-0.333-0.031-0.359 0.021-0.744 0.079-1.208 0.025-0.219 0.077-0.396 0.088-0.635 0-0.053 0-0.131 0-0.188 0-0.407-0.303-0.74-0.667-0.74-0.369 0-0.667 0.333-0.667 0.74v0.021c0 0.052 0 0.119 0 0.167 0.011 0.239 0.063 0.416 0.088 0.635 0.057 0.464 0.105 0.849 0.079 1.208-0.041 0.131-0.115 0.251-0.219 0.344l-0.016 0.281c-2.12 0.172-4.099 1.12-5.552 2.672-0.083-0.057-0.161-0.115-0.24-0.172-0.119 0.016-0.239 0.052-0.395-0.036-0.297-0.204-0.573-0.48-0.901-0.813-0.151-0.161-0.26-0.312-0.437-0.463-0.043-0.037-0.104-0.084-0.147-0.12-0.135-0.104-0.296-0.167-0.463-0.177-0.209-0.011-0.401 0.079-0.532 0.235-0.229 0.292-0.156 0.729 0.161 0.984l0.011 0.005 0.141 0.109c0.187 0.141 0.359 0.213 0.552 0.323 0.396 0.251 0.724 0.453 0.989 0.699 0.099 0.109 0.12 0.301 0.131 0.385l0.213 0.187c-1.177 1.772-1.661 3.907-1.36 6.011l-0.276 0.079c-0.073 0.099-0.177 0.244-0.287 0.292-0.344 0.109-0.729 0.145-1.192 0.192-0.219 0.021-0.407 0.011-0.641 0.052-0.052 0.011-0.12 0.032-0.177 0.041l-0.004 0.005h-0.011c-0.391 0.095-0.647 0.459-0.563 0.813 0.077 0.353 0.463 0.572 0.859 0.484h0.011l0.011-0.005 0.172-0.036c0.229-0.063 0.396-0.152 0.599-0.229 0.437-0.156 0.808-0.292 1.161-0.344 0.147-0.011 0.308 0.093 0.38 0.136l0.292-0.048c0.651 2.011 2.016 3.72 3.839 4.792l-0.12 0.292c0.047 0.115 0.095 0.265 0.057 0.375-0.125 0.339-0.349 0.693-0.599 1.084-0.125 0.181-0.251 0.323-0.36 0.531-0.025 0.052-0.057 0.131-0.083 0.183-0.172 0.364-0.047 0.787 0.281 0.948 0.333 0.156 0.744-0.011 0.921-0.38 0.027-0.052 0.063-0.12 0.084-0.172 0.093-0.213 0.125-0.401 0.192-0.609 0.172-0.443 0.271-0.907 0.516-1.199 0.068-0.077 0.172-0.109 0.287-0.135l0.151-0.276c1.975 0.76 4.161 0.765 6.145 0.015l0.141 0.256c0.115 0.036 0.24 0.057 0.339 0.208 0.183 0.307 0.307 0.677 0.459 1.12 0.067 0.208 0.099 0.396 0.192 0.609 0.021 0.047 0.057 0.12 0.084 0.172 0.176 0.369 0.588 0.536 0.916 0.375 0.333-0.156 0.459-0.579 0.287-0.948-0.027-0.052-0.063-0.125-0.088-0.177-0.109-0.208-0.235-0.348-0.355-0.531-0.255-0.391-0.464-0.719-0.593-1.057-0.052-0.172 0.009-0.276 0.052-0.391-0.027-0.031-0.079-0.193-0.109-0.271 1.828-1.084 3.192-2.803 3.839-4.828 0.083 0.015 0.233 0.041 0.285 0.052 0.1-0.068 0.188-0.152 0.371-0.141 0.353 0.052 0.724 0.188 1.161 0.344 0.203 0.079 0.369 0.167 0.599 0.229 0.047 0.016 0.115 0.027 0.172 0.036l0.011 0.005h0.011c0.396 0.089 0.781-0.129 0.859-0.484 0.084-0.355-0.172-0.719-0.563-0.812zM21.864 12.932l-2.599 2.328v0.011c-0.353 0.308-0.219 0.885 0.229 1.011l0.005 0.011 3.369 0.968c0.073-0.744 0.027-1.5-0.145-2.229-0.167-0.739-0.459-1.452-0.86-2.099zM16.516 20.036c-0.104-0.197-0.313-0.317-0.537-0.312-0.208 0.011-0.4 0.125-0.5 0.312l-1.692 3.057c1.437 0.491 3 0.491 4.437 0l-1.693-3.057zM19.031 18.312c-0.119-0.025-0.244-0.005-0.359 0.048-0.281 0.135-0.412 0.473-0.287 0.76v0.005l1.344 3.249c1.287-0.817 2.265-2.047 2.776-3.484l-3.469-0.588z'/>"];

exports.cibKubernetes = cibKubernetes;
//# sourceMappingURL=cib-kubernetes.js.map
