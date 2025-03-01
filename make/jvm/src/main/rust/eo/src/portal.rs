/*
 * SPDX-FileCopyrightText: Copyright (c) 2016-2025 Objectionary.com
 * SPDX-License-Identifier: MIT
 */

use jni::JNIEnv;
use jni::objects::{JByteArray, JClass, JObject, JValue};

pub mod eo_enum;

pub struct Portal<'local> {
    pub java_env: JNIEnv<'local>,
    _java_class: JClass<'local>,
    java_obj: JObject<'local>
}

impl<'local> Portal<'_> {
    pub fn new(java_env: JNIEnv<'local>, _java_class: JClass<'local>, java_obj: JObject<'local>) -> Portal<'local> {
        Portal {
            java_env,
            _java_class,
            java_obj
        }
    }

    pub fn find(&mut self, att: &str) -> Option<u32> {
        let jstr = JObject::from(self.java_env.new_string(att).ok()?);
        let called = self.java_env
           .call_method(
               &self.java_obj,
               "find",
               "(Ljava/lang/String;)I",
               &[JValue::from(&jstr)]
           );
        return if called.is_err() {
            self.java_env.exception_clear().ok()?;
            None
        } else {
            called.unwrap().i().ok().map(|value| value as u32)
        }
    }

    pub fn put(&mut self, v: u32, bytes: &[u8]) -> Option<()> {
        let jbytes = JObject::from(
            self.java_env.byte_array_from_slice(bytes).ok()?
        );
        let java_val =  self.java_env
            .call_method(
                &self.java_obj,
                "put",
                "(I[B)V",
                &[JValue::Int(v as i32), JValue::from(&jbytes)]
            );
        return if java_val.is_err() {
            self.java_env.exception_clear().ok()?;
            None
        } else {
            java_val.unwrap().v().ok()
        }
    }

    pub fn bind(&mut self, v1: u32, v2: u32, name: &str) -> Option<()> {
        let java_val =  self.java_env
            .call_method(
                &self.java_obj,
                "bind",
                "(IILjava/lang/String;)V",
                &[
                    JValue::Int(v1 as i32),
                    JValue::Int(v2 as i32),
                    JValue::from(
                        &JObject::from(self.java_env.new_string(name).ok()?)
                    )
                ]
            );
        return if java_val.is_err() {
            self.java_env.exception_clear().ok()?;
            None
        } else {
            java_val.unwrap().v().ok()
        };
    }

    pub fn copy(&mut self, v: u32) -> Option<u32> {
        let java_val = self.java_env
            .call_method(
                &self.java_obj,
                "copy",
                "(I)I",
                &[
                    JValue::Int(v as i32),
                ]
            );
        return if java_val.is_err() {
            self.java_env.exception_clear().ok()?;
            None
        } else {
            java_val.unwrap().i().ok().map(|x| x as u32)
        };
    }

    pub fn dataize(&mut self, v: u32) -> Option<Vec<u8>> {
        let called = self.java_env
            .call_method(
                &self.java_obj,
                "dataize",
                "(I)[B",
                &[
                    JValue::Int(v as i32),
                ]
            );
        if called.is_err() {
            self.java_env.exception_clear().ok()?;
            return None;
        }
        let java_array = JByteArray::from(
            called.unwrap().l().ok()?);
        let size = self.java_env.get_array_length(&java_array).ok()?;
        let mut bytes = vec![0; size.try_into().ok()?];
        if self.java_env.get_byte_array_region(&java_array, 0, &mut bytes[0..]).is_err() {
            return None;
        }
        let unsigned = unsafe { &*(&bytes[0..] as *const _  as *const [u8]) };
        return Some(unsigned.to_vec());
    }
}
