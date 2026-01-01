/*
 * SPDX-FileCopyrightText: Copyright (c) 2016-2026 Objectionary.com
 * SPDX-License-Identifier: MIT
 */

pub enum EO {
    EOVertex(u32),
    EONumber(f64),
    EOString(String),
    EORaw(Box<[u8]>),
    EOError(String),
}

impl EO {
    pub fn eo2vec(&self) -> Vec<u8> {
        match self {
            EO::EOVertex(v) => {
                let mut res: Vec<u8> = vec![0; 1 + 4];
                res[0] = 0;
                res[1..].copy_from_slice(&v.to_be_bytes());
                res
            }
            EO::EONumber(x) => {
                let mut res = vec![0; 1 + 8];
                res[0] = 1;
                res[1..].copy_from_slice(&x.to_be_bytes());
                res
            }
            EO::EOString(content) => {
                let content_bytes = content.clone().into_bytes();
                let mut res: Vec<u8> = vec![0; 1 + content_bytes.len()];
                res[0] = 3;
                res[1..].copy_from_slice(&content_bytes);
                res
            }
            EO::EORaw(content) => {
                let mut res: Vec<u8> = vec![0; 1 + content.len()];
                res[0] = 4;
                res[1..].copy_from_slice(&content.to_vec());
                res
            }
            EO::EOError(cause) => {
                let cause_bytes = cause.clone().into_bytes();
                let mut res: Vec<u8> = vec![0; 1 + cause_bytes.len()];
                res[0] = 5;
                res[1..].copy_from_slice(&cause_bytes);
                res
            }
        }
    }
}
