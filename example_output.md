```
offsets-of JSC::JSArray
JSC::JSArray[72] {
     JSC::JSNonFinalObject                                                        JSC::JSNonFinalObject                 = char[48] at   <base type>       
         JSC::JSObject                                                            JSC::JSObject                         = char[32] at   <base type>       
             JSC::JSCell                                                          JSC::JSCell                           = char[16] at   <base type>       
>                const JSC::ClassInfo *                                           m_classInfo                           = char[ 8] at           0x0  (0) <
                 JSC::WriteBarrier<JSC::Structure>                                m_structure                           = char[ 8] at           0x8  (8)  
                     JSC::WriteBarrierBase<JSC::Structure>                        JSC::WriteBarrierBase<JSC::Structure> = char[ 8] at   <base type>       
>                        JSC::JSCell *                                            m_cell                                = char[ 8] at           0x8  (8) <
             JSC::StorageBarrier                                                  m_propertyStorage                     = char[ 8] at          0x10 (16)  
>                JSC::PropertyStorage (aka JSC::WriteBarrierBase<JSC::Unknown> *) m_storage                             = char[ 8] at          0x10 (16) <
             JSC::WriteBarrier<JSC::Structure>                                    m_inheritorID                         = char[ 8] at          0x18 (24)  
                 JSC::WriteBarrierBase<JSC::Structure>                            JSC::WriteBarrierBase<JSC::Structure> = char[ 8] at   <base type>       
>                    JSC::JSCell *                                                m_cell                                = char[ 8] at          0x18 (24) <
         JSC::WriteBarrier<JSC::Unknown> [2]                                      m_inlineStorage                       = char[16] at          0x20 (32)  
>            <range type>                                                         None                                  = char[ 8] at <range type?>      <
>    unsigned int                                                                 m_vectorLength                        = char[ 4] at          0x30 (48) <
>    unsigned int                                                                 m_indexBias                           = char[ 4] at          0x34 (52) <
>    JSC::ArrayStorage *                                                          m_storage                             = char[ 8] at          0x38 (56) <
>    JSC::SparseArrayValueMap *                                                   m_sparseValueMap                      = char[ 8] at          0x40 (64) <
}
```