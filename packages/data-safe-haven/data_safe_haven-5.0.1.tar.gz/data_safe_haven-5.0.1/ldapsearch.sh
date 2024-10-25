ldapsearch -x -b "CN=jim.madge,OU=users,DC=daimyo,DC=develop,DC=turingsafehaven,DC=ac,DC=uk" -H ldap://identity.hojo.daimyo.develop.turingsafehaven.ac.uk:1389

ldapsearch -x -D "CN=jim.madge,OU=users,DC=daimyo,DC=develop,DC=turingsafehaven,DC=ac,DC=uk" -b "DC=daimyo,DC=develop,DC=turingsafehaven,DC=ac,DC=uk" -W -H ldap://identity.hojo.daimyo.develop.turingsafehaven.ac.uk:1389

ldapwhoami -x -D "CN=jim.madge,OU=users,DC=daimyo,DC=develop,DC=turingsafehaven,DC=ac,DC=uk" -W -H ldap://identity.hojo.daimyo.develop.turingsafehaven.ac.uk:1389
